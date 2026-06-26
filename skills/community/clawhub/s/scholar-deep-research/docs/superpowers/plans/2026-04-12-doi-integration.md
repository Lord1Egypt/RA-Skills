# DOI Integration for extract_pdf.py

> **For agentic workers:** Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add `--doi` flag to `extract_pdf.py` that resolves DOIs to PDFs via paper-fetch (optional) or Unpaywall fallback.

**Architecture:** Discovery chain: `PAPER_FETCH_SCRIPT` env var → `~/.claude/skills/paper-fetch/scripts/fetch.py` convention path → built-in Unpaywall fallback. Output envelope gains `fetch_meta` field with DOI metadata.

---

### Task 1: Add --doi flag and paper-fetch discovery

**Files:**
- Modify: `scripts/extract_pdf.py`

- [ ] **Step 1: Add `--doi` to the mutually exclusive input group**

Add `--doi` alongside `--input` and `--url` in the existing `add_mutually_exclusive_group`.

- [ ] **Step 2: Add `_find_paper_fetch()` discovery function**

Returns the path to `fetch.py` if found, else `None`. Check `PAPER_FETCH_SCRIPT` env var first, then `~/.claude/skills/paper-fetch/scripts/fetch.py`.

- [ ] **Step 3: Add `_fetch_via_paper_fetch(doi, fetch_script)` function**

Shell out to `python <fetch_script> <doi> --format json --out <tmpdir>`, parse the JSON envelope, return `(pdf_path, fetch_meta_dict)` or raise on failure.

- [ ] **Step 4: Add `_fetch_via_unpaywall(doi)` fallback function**

GET `https://api.unpaywall.org/v2/{doi}?email={SCHOLAR_MAILTO}`, extract `best_oa_location.url_for_pdf`, download the PDF to a tempfile. Return `(pdf_path, fetch_meta_dict)` with `source: "unpaywall_fallback"`. Error if no OA URL found (`no_open_access_pdf`).

- [ ] **Step 5: Wire `--doi` into `main()`**

If `args.doi`: try paper-fetch first, fall back to Unpaywall. Set `pdf_path` and `fetch_meta`. After extraction, merge `fetch_meta` into the output data dict.

- [ ] **Step 6: Fix double PdfReader bug**

Remove the redundant `PdfReader` at line 110 — `extract()` already creates its own.

- [ ] **Step 7: Test end-to-end**

```bash
python scripts/extract_pdf.py --doi 10.1038/s41586-020-2649-2 --schema
python scripts/extract_pdf.py --doi 10.1038/s41586-020-2649-2
```

- [ ] **Step 8: Commit**

### Task 2: Update SKILL.md

**Files:**
- Modify: `SKILL.md`

- [ ] **Step 1: Add `PAPER_FETCH_SCRIPT` to env var table (line ~312)**
- [ ] **Step 2: Update Phase 3 deep-read section to show `--doi` usage**
- [ ] **Step 3: Update script inventory table to mention DOI support**
- [ ] **Step 4: Commit**

### Task 3: Update READMEs

**Files:**
- Modify: `README.md`, `README_CN.md`

- [ ] **Step 1: Add `--doi` to usage examples and env var docs in both files**
- [ ] **Step 2: Commit**
