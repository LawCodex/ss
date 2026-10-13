#!/usr/bin/env python3
"""South Sudan: the Ministry of Justice and Constitutional Affairs website (mojca.gov.ss), which
published the Transitional Constitution and the Acts of South Sudan as PDFs, is unreachable; its
files are taken from the Internet Archive (Wayback Machine) copies. Converts them to Markdown.

Usage: python3 ss_fetch.py [--no-download]"""
import os
import re
import sys
import urllib.parse

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ss_text as T  # noqa

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(os.path.dirname(REPO), "_raw", "ss")
RETRIEVED = os.environ.get("LC_RETRIEVED", "2026-10-13")
CDX = ("http://web.archive.org/cdx/search/cdx?url=mojca.gov.ss/wp-content/uploads/*&fl=timestamp,original,statuscode,mimetype"
       "&filter=statuscode:200&filter=mimetype:application/pdf&collapse=urlkey&limit=2000")
SKIP = re.compile(r"Strategic|Introduction|Judicial-Reform|Permanent-Constitution-Making|Table-of-Sections|ACTS-SUPPLEMENT|"
                  r"Commission-for-Truth|Compensation-and-Reparation|Updated-Strategic|Fees-Schedule|Circular|"
                  r"The-Transitional-Constitution-of-the-Repulic", re.I)  # last: duplicate upload of the 2011 text


def items():
    p = os.path.join(RAW, "cdx.txt")
    if "--no-download" not in sys.argv or not os.path.exists(p):
        r = requests.get(CDX, headers={"User-Agent": T.UA}, timeout=180)
        r.raise_for_status()
        open(p, "w").write(r.text)
    out = {}
    for line in open(p):
        ts, orig, st, mt = line.split()
        name = urllib.parse.unquote(orig.rsplit("/", 1)[-1])
        if SKIP.search(name):
            continue
        key = re.sub(r"^https?://", "", orig)
        out[key] = (ts, orig, name)
    return list(out.values())


def title_of(name):
    t = name[:-4].replace("-", " ").replace("_", " ")
    t = re.sub(r"\bRepulic\b", "Republic", t)
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"\s+final$", "", t)
    t = re.sub(r"\bAct Act\b", "Act", t)
    return t


def main():
    seen = set()
    n = 0
    for ts, orig, name in sorted(items(), key=lambda x: x[2]):
        arch = "https://web.archive.org/web/%sid_/%s" % (ts, orig)
        pdf = os.path.join(RAW, "pdf", name)
        if "--no-download" not in sys.argv:
            T.fetch(arch, pdf, delay=3, check_pdf=True)
        if not os.path.exists(pdf) or not T.pdf_ok(pdf):
            print("MISSING", name)
            continue
        pages, _ = T.pdf_text(pdf, "eng", ocr=False)
        txt = "\n".join(pages)
        if len(txt.strip()) < 500 or T.text_quality(txt) < 0.75:
            print("SKIP no/garbled text", name)
            continue
        title = title_of(name)
        if title.upper() == title:
            title = title.title().replace(" Of ", " of ").replace(" The ", " the ")
        key = T.slug(re.sub(r"^the ", "", title, flags=re.I))
        if key in seen:
            print("dup", name)
            continue
        seen.add(key)
        m = re.search(r"\b(19|20)\d\d\b", title)
        year = m.group(0) if m else None
        num = re.search(r"\b(\d{1,3}) of ((19|20)\d\d)\b", title)
        is_const = bool(re.match(r"^(The )?(Interim|Transitional) Constitution", title))
        lines = T.clean_pages(pages)
        starts = (r"^We,? the [Pp]eople", r"^WE,? THE PEOPLE", r"^Preamble$", r"^PREAMBLE$") if is_const else \
            (r"^AN ACT\b", r"^An Act\b", r"^ENACTED\b", r"^BE IT ENACTED\b", r"^In accordance with\b", r"^IN ACCORDANCE WITH\b")
        body = T.structure(T.drop_toc(lines, starts=starts), "en", art_word="Article" if is_const else "Section")
        meta = {"title": title, "identifier": ("Act No. %s of %s" % (num.group(1), num.group(2))) if num else None,
                "type": "constitution" if is_const else ("regulation" if "Regulation" in title else "act"),
                "jurisdiction": "ss", "language": "en", "year": int(year) if year else None,
                "status": "unknown", "source": orig, "archived_source": arch, "retrieved": RETRIEVED}
        if is_const:
            path = os.path.join(REPO, "constitution", key + ".md")
            if "2005" in title:
                meta["status"] = "repealed"
        else:
            path = os.path.join(REPO, "acts", year or "undated", key + ".md")
        T.write_md(path, meta, title, body)
        n += 1
        print("ok", title)
    print("written", n)


if __name__ == "__main__":
    main()
