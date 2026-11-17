# Douyin

The adapter reads the user's own favorites through an explicitly authenticated browser page. It does not accept cookies or private request headers in configuration, and it does not reproduce the site's request-signing algorithm in Python. Ephemeral page access data stays in process memory and is omitted from references, diagnostics, logs, and committed fixtures.

## Structural compatibility evidence

On 2026-08-08 an authorized Chrome session was inspected for field shape only. No user identity, post text, media, URL, token, signature, or raw response was retained. The observed favorites state provided:

- authenticated server-rendered session state and a self-profile route;
- a favorites tab with stable video/note links;
- response shapes compatible with `aweme_list`, cursor/has-more pagination, video data, ordered images, and availability;
- optional caption/subtitle candidate fields, which do not by themselves prove that a usable text track exists.

The committed `tests/fixtures/sanitized/douyin.json` recreates the required shapes entirely with synthetic identifiers, prose, and `example.invalid` URLs. It is regression data, not a recording of the account.

## Processing rules

- A usable timestamped text track is preserved as a native subtitle source.
- Caption metadata without usable timestamped text is only a probe result; the default video path remains local ASR plus adaptive frame OCR.
- ASR and frame-OCR segments pass through timeline fusion so a spoken burned caption is not duplicated while visual-only labels remain.
- One-image posts remain image posts; multi-image posts remain ordered galleries with OCR rendered immediately below each image.
- Page-exposed high-quality image URLs are preferred. A fallback quality marker is recorded only when the preferred field is absent.
- Static downloads pass the bounded MIME/length/hash store and local image decoding and dimension checks before becoming assets.
- A missing identity, item list, completeness marker, image dimension, cursor, or usable media URL is a typed adapter failure. It never turns a partial result into a complete enumeration.

## Diagnostics and recovery

`douyin.needs_auth` requires the dedicated browser login flow. Layout or response drift produces `douyin.layout_changed`; re-enumerate only after inspecting the sanitized code and updating the adapter/fixture. Media URLs are ephemeral, so retry media failures by enumerating again rather than persisting page access data.
