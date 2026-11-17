---
name: underlimit
description: Shrink a scanned PDF to fit an upload size limit (a government, visa, university or job portal's 2 MB or 5 MB cap), offline, without sending the document anywhere. Use when the user has a PDF that is too big to upload, asks to compress or shrink a scanned PDF, or must get IDs, contracts, tax forms or other scans under a file-size limit.
metadata:
  openclaw:
    requires:
      bins: [node, npx]
    homepage: https://mirceamitu.github.io/underlimit/
---

# Underlimit

> Shrink a scanned PDF under an upload limit, offline. One command; the answer is one JSON object and an exit code. The document never leaves the machine, so it is safe for passports, IDs, contracts and tax forms.

Pages of ink on paper become black & white with CCITT Group 4 (fax compression), which is several times smaller than JPEG for text; pages with photos stay JPEG. A 30 MB scan typically ends up around 1 to 2 MB at a full 300 DPI.

## First: can you run commands on the user's own computer?

The CLI must run where the PDF already is. If you are a chat assistant running in the cloud, or a sandbox without access to the user's files, **do not ask the user to upload the PDF to you**. Uploading it is the risk this tool exists to avoid. Send them to the web page instead:

> **https://mirceamitu.github.io/underlimit/**: open it, drop the PDF in, choose the limit, download the result. It runs entirely in their browser, and nothing is uploaded. They can also save the page and use it offline.

If the user has already shared the PDF with you, still point them to the page rather than processing it in a cloud sandbox.

Only continue below if you can run shell commands on the machine that holds the PDF.

## Run it

```sh
npx -y underlimit scan.pdf --limit 2
```

- Needs Node 20+. `-y` skips npx's install prompt, which would block a non-interactive shell. The first run downloads pdf.js and a native canvas build (tens of MB); later runs are cached.
- `--limit` is in decimal MB: `--limit 2` is 2,000,000 bytes, the strict reading of "2 MB", so the file passes either way.
- `--min-dpi 300|200|150`: the lowest resolution allowed (default 300).
- `-o out.pdf`: where to write (default: `scan.under-2MB.pdf` next to the input). It never overwrites the input.
- Progress (`page 3/18`) goes to stderr, at about 0.5 s per page. Give long documents a longer timeout.
- Pin a version so behaviour doesn't change between runs: `npx -y underlimit@1.1.0 ...`.
- `--help` prints the full contract.

## Read the result

Stdout is one JSON object. Branch on the exit code.

**Exit 0, it fits.** Upload `output.path`; `output.bytes` is its exact size. In `pages`, `g4` is a black & white page and `jpeg` a photo page kept in grey or colour.

```json
{"fits":true,"alreadyFits":false,"limitBytes":2000000,
 "input":{"path":"/home/me/scan.pdf","bytes":12299532,"pages":6},
 "output":{"path":"/home/me/scan.under-2MB.pdf","bytes":1530530,"dpi":300},
 "pages":[{"n":1,"kind":"g4"},{"n":2,"kind":"g4"},{"n":3,"kind":"g4"},{"n":4,"kind":"g4"},{"n":5,"kind":"g4"},{"n":6,"kind":"jpeg"}],
 "warnings":[]}
```

**Exit 0, already under the limit.** Nothing is written: upload the original.

```json
{"fits":true,"alreadyFits":true,"limitBytes":50000000,
 "input":{"path":"/home/me/scan.pdf","bytes":12299532,"pages":6},"output":null,"warnings":[]}
```

**Exit 1, can't fit at `--min-dpi`.** Nothing is written. `closest` is the best miss. `rescue` is the lower `--min-dpi` that would fit, or `null` if none does.

```json
{"fits":false,"limitBytes":1000000,
 "input":{"path":"/home/me/scan.pdf","bytes":12299532,"pages":6},"output":null,
 "closest":{"dpi":300,"bytes":1530530},"rescue":{"dpi":200,"bytes":651274},"warnings":[]}
```

**Exit 2, error.** Nothing is written.

```json
{"error":{"code":"encrypted","message":"The PDF is password-protected. Ask the user for an unprotected copy."}}
```

Codes: `usage`, `not_found`, `not_pdf`, `encrypted`, `output_is_input`, `internal`.

## What to do

1. Run with the portal's limit.
2. **Exit 0:** upload `output.path`, or the original if `alreadyFits`. Tell the user about any `warnings`.
3. **Exit 1 with a `rescue`:** 200 DPI is still readable on screen, 150 DPI less so. Ask the user, then rerun with `--min-dpi <rescue.dpi>`. **With `rescue: null`:** suggest splitting the document into two uploads, or check whether the portal allows a higher limit.
4. **Exit 2:** act on `error.code`. For example, `encrypted` means asking the user for an unprotected copy.

## Limits

- It is for scans. Every output page is an image, so a PDF made on a computer loses its selectable text. The `warnings` name those pages, e.g. `"page 2 had selectable text, which the output does not keep"`. If the text matters, don't use the output.
- Password-protected PDFs can't be opened (exit 2, `encrypted`).
- No network access, ever: no telemetry, no update checks.
