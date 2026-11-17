# Files, documents, voice and OCR

Read to download a file, transcribe a voice note, search inside documents (`content:`) or read a scan.

The ids below are made up — use the real ones from the previous answer.

```sh
tg personal messages download -1001234567890 4242 --output-dir /tmp/tg --json  # the message's file; answers its path
tg personal messages download -1001234567890 --all --output-dir /tmp/tg --jsonl --timeout 10m  # every file of the chat; run it again to continue
tg personal messages transcribe -1001234567890 4242 --json  # a voice note as text; can take up to a minute; never download a model yourself
```

`content:invoice` searches indexed text extracted from attachments or supplied by an agent. Extraction supports
plain text (UTF-8, BOM-marked UTF-16 and high-confidence legacy encodings), ODT, ODS, XLSX,
PPTX, EPUB, Word and PDFs with text layers; scans and photos need agent-supplied text.
Start with local extraction for digital documents. Formulas are not calculated and embedded
images are not OCRed; uncertain encodings need inspection or conversion. With several attachments,
choose `--attachment`, starting at 1.

By default, perform OCR yourself with the agent's file-reading and vision tools. After downloading
and local extraction, handle `needs-agent` items: find each `local_path` with `attachments list
is:needs_text`, read the image or scan, and save literal transcription with `attachments update`.
Retain the message locator and attachment number; verify the result with a `content:` query.
Do not silently substitute a separate model API call. The owner explicitly selects API processing
for bulk work. If your tools cannot access the file, report that limitation; a path on an MCP
server does not transfer the file to a remote agent.

When the owner explicitly selects bulk API processing, use `attachments extract --ocr` with
`models.ocr.provider` and `models.ocr.model`, the ordinary `models keys set` credential command and
`--concurrency` (1–8, default4). `--limit` is1–500files, default100; continue using cursor.
Do not add --ocr automatically to ordinary extraction. Scanned PDFs need optional unpdf and
@napi-rs/canvas, at most20pages. Inspect failed counts and statuses; retries reuse successful
file caches. Agent text and old indexed text survive failed or cancelled API OCR.

```sh
tg personal attachments extract --chat "Book club" --download --output-dir ./files
tg personal search messages 'content:invoice'
tg personal attachments list 'chat:"Book club" is:needs_text'
tg personal attachments update "Book club" 204 --text-file ./scan.txt
```

`--download` requires `--output-dir`; without them extraction reads retained files. `list` exposes retained paths and text status, not text contents.

Extract files with `attachments extract --chat <chat> --from-dir ./files`, or add `--extract`
to `messages download`. For MCP discover `attachments extract`, then use `tg_write`; bounded
extraction returns a continuation `cursor` and metadata without file text. After an explicitly
authorized fetch, `--catch-up` prepares local search within `--catch-up-chunks`,
`--catch-up-messages` and `--catch-up-time`; `--no-catch-up` overrides profile `search_catch_up`.
from_dir and retained-file transfer protect known credential files/folders, CLI folders and the message store;
MCP output_dir protects these locations too. Ordinary hidden working folders are allowed.
Local PDF text has no fixed page-count limit or separate 30-second cutoff; cancellation and file/text budgets apply.
Local voice requires complete mono/stereo Ogg Opus without a ten-minute cutoff; long recordings need more memory.
No models are downloaded and no remote provider is called.
These commands and job metadata are also available through MCP discovery and read/write gateways.

Remote agents can request retained bytes: discover attachments show through tg_tools_search
and invoke tg_read. Assemble chunks by next_offset_bytes, pass expected_fingerprint and verify SHA256.
If the client cannot open a PDF, request every page using page:1..pdf.page_count; optional
unpdf/@napi-rs/canvas render locally. The page returns image content; if only metadata is visible,
request format:base64 and display the PNG with the agent's image tools. Inspect the actual pixels
of every page; receiving Base64 is not reading. pdf.sourceSha256 identifies the source PDF,
top-level sha256 the PNG. No external OCR API or automatic indexing: save your own literal
transcription with attachments update and verify content search. If pixels remain inaccessible,
report that limit and never substitute old indexed text. Quality depends on resolution, language and layout.
