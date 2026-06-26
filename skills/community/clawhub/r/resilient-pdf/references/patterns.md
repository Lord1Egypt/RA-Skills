# Resilient PDF patterns

## Goal

Provide a repeatable fallback path when native PDF analysis fails, hangs, times out, or rejects a file due to size or environment limits.

## Use this skill when

- the built-in `pdf` tool fails or hangs
- a local PDF is too large for provider-native upload limits
- a remote PDF should be downloaded and processed locally first
- the machine is missing classic PDF utilities like `pdftotext`
- the task needs extracted markdown/text plus optional chunking before summarization

## Preferred extraction path

1. If the source is remote, download the PDF locally first or use the script's `--url` mode
2. Use local extraction with `uvx --from 'markitdown[pdf]' markitdown`
3. Write the extracted content to a local markdown file
4. If the output is large, chunk it into manageable markdown pieces
5. Optionally produce a lightweight first-pass summary artifact to guide later reading
6. Read the extracted file or chunks and summarize with the current model, or hand chunks to another summarizer workflow

## Why this path

- avoids provider PDF size limits
- avoids dependence on `pdftotext`, `pdfinfo`, or poppler being installed
- reproducible on hosts where Python exists but PDF tooling is sparse
- works well as a fallback for large research papers, manuals, and system cards

## Failure handling

If `uvx` is missing, the standard install hint is:

```bash
python3 -m pip install --user --break-system-packages uv
```

If markitdown without PDF extras is present, prefer invoking it through:

```bash
uvx --from 'markitdown[pdf]' markitdown ...
```

That avoids depending on a separately managed local environment.

## Chunking guidance

Default chunking target in the helper script is intentionally large because local files are cheap to store. Adjust when needed:

- small PDF or targeted read: no chunking
- medium PDF: 80k to 150k chars per chunk
- very large PDF: 50k to 100k chars per chunk with overlap

Use overlap when preserving context across section boundaries matters.

## Summary guidance

For user-facing summaries:
- treat the script-generated summary as a navigation aid, not a final answer
- start with the main headline
- separate hard findings from interpretation
- call out quoted or numeric claims carefully
- mention when observations come from earlier model versions versus final versions

## Safety and scope

- Do not assume extracted markdown is perfectly clean. Verify important claims against the extracted text.
- Treat shell install commands as explicit operator actions, not silent side effects.
- Prefer local file paths inside the workspace.
