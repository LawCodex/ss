# South Sudan (SS) — legislation as Markdown

Part of [LawCodex](https://github.com/LawCodex): the legislation of every country as plain Markdown in git.

Legislation of the Republic of South Sudan, in **English** (the official language), as published by the
**Ministry of Justice and Constitutional Affairs** (MoJCA, mojca.gov.ss) in its "Laws of South Sudan" PDF series:

* the **Transitional Constitution of the Republic of South Sudan, 2011** (text as adopted in 2011) and, for
  reference, the repealed **Interim Constitution of Southern Sudan, 2005**;
* **Acts** of the (Southern) Sudan Legislative Assembly and of the National Legislature, 2006–2017, plus one set
  of regulations.

The MoJCA website is not reachable; its PDF files were retrieved from the **Internet Archive** (Wayback Machine)
copies of the official URLs (`archived_source` in the front matter; `source` is the original MoJCA URL).

Retrieved 2026-10-13.

<!-- COUNTS -->
| Directory | Files |
|---|---|
| `acts/` | 62 |
| `constitution/` | 2 |
| **Total** | **64** |
<!-- /COUNTS -->

## Structure

```
constitution/transitional-constitution-of-the-republic-of-south-sudan-2011.md
constitution/interim-constitution-of-southern-sudan-2005.md     (repealed)
acts/<year>/<slug>.md
```

File names are slugs of the MoJCA file names (e.g. `penal-code-act-9-of-2008.md`). `identifier` gives the Act
number when it is part of the title; `status` is `unknown` for Acts.

## Sources

| Source | URL | Used for |
|---|---|---|
| Ministry of Justice and Constitutional Affairs — Laws of South Sudan (via the Internet Archive) | https://mojca.gov.ss/wp-content/uploads/2023/03/ (Wayback: `https://web.archive.org/web/<timestamp>id_/<url>`) | Constitution, Acts |
| Transitional National Legislative Assembly (links to the MoJCA files) | https://nla.gov.ss/ | discovery |

## Not covered / known gaps

* **Constitutional amendments are not incorporated**: the Transitional Constitution has been amended several times
  (2013, 2015, 2018 — incorporation of the peace agreements — and later extensions of the transitional period);
  only the 2011 text is published here.
* Only the ~70 Acts that the MoJCA put online are covered (mostly 2006–2013); Acts passed after 2013 (except the
  National Security Service Act 2014 and the Labour Act 2017) are missing.
* 5 PDFs are scans without a text layer and were not converted (no OCR): Investment Promotion Act 2009, Judicial
  Service Council Act 2008, Local Government Act 2009, NGO Act Regulations 2016, SPLA (Amendment) Act 2009.
* The TNLA website currently redirects its pages to a third-party URL-shortener domain; it was not used beyond the
  list of MoJCA links on its home page.

## Copyright

Acts and the Constitution of South Sudan are official public texts published by the Government of South Sudan.
The Markdown conversion is provided as is, for information; the authoritative texts are the official prints.

## Regenerate

```
python3 -m pip install -r scripts/requirements.txt   # plus poppler (pdftotext)
python3 scripts/ss_fetch.py        # Wayback CDX listing + downloads cached in ../_raw/ss
python3 scripts/ss_readme.py
```
