# Xiaohongshu / RedNote

The adapter reads the user's own saved notes through an explicitly authenticated browser page. It does not accept cookies or private request headers in configuration, and it does not reproduce the site's request-authentication algorithm in Python. Ephemeral page access data stays in process memory and is omitted from references, diagnostics, logs, and committed fixtures.

## Structural compatibility evidence

On 2026-08-08 an authorized Chrome session was inspected for field shape only. No user identity, note text, media, URL, token, or raw response was retained. The observed saved-note state provided:

- cursor/has-more pagination metadata;
- stable saved-entry identities and `normal`/`video` type labels;
- detail fields for title, description, author, ordered `imageList`, video metadata, and availability;
- image dimensions plus `urlDefault`, fallback URLs, and alternative scene URLs.

The committed `tests/fixtures/sanitized/xiaohongshu.json` recreates those shapes entirely with synthetic identifiers, prose, and `example.invalid` URLs. It is regression data, not a recording of the account.

## Processing rules

- Pure-text notes remain articles.
- One-image notes remain image posts; multi-image notes remain ordered galleries.
- `imageList[].urlDefault` is preferred and recorded as a `page-default` rendition rather than an unverified original. Other fields receive a fallback marker.
- Static downloads pass the bounded MIME/length/hash store, local image decoding, and source-aspect-ratio checks before becoming assets. Page renditions may be lower resolution than the source dimensions while preserving geometry.
- Ordered image assets become ordered content blocks. Markdown renders OCR immediately below the corresponding image.
- Videos probe the page for a real text track, but the normal no-track path is local ASR plus adaptive frame OCR and timeline fusion.
- A missing identity, item list, completeness marker, image dimension, or usable media URL is a typed adapter failure. It never turns a partial result into a complete enumeration.

## Diagnostics and recovery

`xiaohongshu.needs_auth` requires the dedicated browser login flow. Layout or response drift produces `xiaohongshu.layout_changed`; re-enumerate only after inspecting the sanitized code and updating the adapter/fixture. Media URLs are ephemeral, so retry media failures by enumerating again rather than persisting page access data.
