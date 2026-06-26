---
name: resilient-pdf
description: Recover PDF extraction and summarization workflows when native PDF handling fails, hangs, times out, or rejects large files. Use when working with local or remote PDFs, especially research papers, manuals, system cards, or other long documents that exceed provider limits or fail in the built-in `pdf` tool. Supports URL download, local extraction via `uvx` + `markitdown[pdf]`, optional chunking, and first-pass summary artifacts.
---

# Resilient PDF

Use this skill as a fallback workflow for PDFs that break normal analysis paths.

## Overview

Prefer the built-in `pdf` tool first when it is likely to work. If it fails, hangs, times out, or the file is too large, switch to this local workflow.

Read `references/patterns.md` if you need the rationale, chunking heuristics, or fallback guidance.

## Workflow

1. Confirm the PDF source.
   - If remote, download it into the workspace first.
   - If local, confirm the path and file size.

2. Decide whether the normal path is already broken.
   - Trigger this skill when the built-in `pdf` tool aborts, provider-native upload fails, or file limits make direct analysis unlikely to work.

3. Run the helper extractor.
   - Use `scripts/extract_pdf.py` to extract markdown locally.
   - Use `--url` to download a remote PDF first.
   - Add `--chunk-dir` when the output will be too large to read in one pass.
   - Add `--summary-out` to generate a lightweight first-pass summary artifact.

4. Inspect the extracted output.
   - Read the head, table of contents, or key sections first.
   - Do not trust a summary until the extracted text looks sane.

5. Summarize or analyze.
   - For short outputs, read the extracted markdown directly.
   - For long outputs, read selected chunks or key sections.
   - Use the generated first-pass summary as a navigation aid, not as final truth.
   - Keep quoted claims and numeric claims grounded in the extracted text.

## Helper script

Local file command:

```bash
python3 skills/resilient-pdf/scripts/extract_pdf.py <file.pdf> --out <output.md> --json
```

Remote URL command:

```bash
python3 skills/resilient-pdf/scripts/extract_pdf.py \
  --url <https://example.com/file.pdf> \
  --out <output.md> \
  --download-to <downloaded.pdf> \
  --json
```

Chunked plus summary command:

```bash
python3 skills/resilient-pdf/scripts/extract_pdf.py <file.pdf> \
  --out <output.md> \
  --chunk-dir <chunk-dir> \
  --summary-out <summary.md> \
  --chunk-chars 120000 \
  --chunk-overlap 4000 \
  --json
```

The script:
- accepts either a local file path or `--url`
- downloads remote PDFs when needed
- looks for `uvx`
- invokes `uvx --from 'markitdown[pdf]' markitdown`
- writes extracted markdown
- optionally writes chunk files
- optionally writes a lightweight first-pass summary markdown file
- emits a machine-readable JSON result

## If dependencies are missing

If `uvx` is not available, tell the operator the exact command to install it:

```bash
python3 -m pip install --user --break-system-packages uv
```

Do not silently install dependencies unless the user asked you to.

## Output expectations

A successful run should give you:
- downloaded PDF path when using `--url`
- extracted markdown path
- byte count
- text character count
- optional chunk paths
- optional first-pass summary path

Use those outputs as the source of truth for later summarization.

## Notes

- This skill does not replace the built-in `pdf` tool. It is the fallback when that path is unreliable.
- Prefer workspace-local outputs so later reads and summaries are reproducible.
- If the extracted markdown is noisy, inspect section headers and sample passages before making strong claims.
