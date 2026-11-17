---
name: tuneviva-practice-score
description: Open a TuneViva catalogue score for practice or retrieve its MusicXML. Use when a user supplies a TuneViva score link or asks to practise a selected catalogue score.
---

# Practise a TuneViva score

## Select the score

Use the numeric ID from the user's TuneViva score URL: `/scores/{id}/{slug}`. If no score is selected, use the public search page `https://tuneviva.com/search?q={url-encoded-query}` and inspect the matching score pages. Search is a web page, not a documented JSON API. Confirm the title, composer and arrangement before choosing among similar results; do not guess IDs or assume arrangements have the same difficulty.

## Check practice availability

Request `GET https://tuneviva.com/api/practice/{id}`. A successful response contains `title`, `scoreURL` (canonical score page path) and `musicxml` (an absolute HTTPS CDN download URL). For example, `/api/practice/70152` returns metadata for the beginner Ode to Joy score. Use the returned title rather than assuming every edition matches this example.

Production requires no account or API key. Staging is access-restricted and is not a public API alternative.

A 404 means the ID is invalid, the score is missing, or no supported MusicXML is available. Do not promise interactive practice for that score. Offer another matching score if useful. On a server error, report that availability could not be checked; avoid repeated automated retries.

## Give the user a practice link

For a supported score, link to `https://tuneviva.com/learn/?score={id}` and retain the original score-page link for its musical details and attribution. The user can open practice in their browser. Microphone or MIDI access requires compatible hardware, browser support and the user's permission; retrieving metadata does not enable these devices.

## Help the user practise

Tap the highlighted on-screen piano keys to try the score without extra hardware. For a two-staff score, Left and Right select the lower and upper staff; Both includes both. These controls select staves, not inferred hand assignments for arbitrary ensemble scores.

“Play” starts playback for listening. For instrument input, use a compatible MIDI keyboard or the “Mic” control. MIDI chords should be played together. Microphone matching is experimental and audio stays on the device; do not promise reliable feedback in every environment. MIDI may appear under “More” on narrow screens and may be unavailable in unsupported browsers.

Use “More” for tempo, restart and full screen. Start slowly with a short passage and increase tempo when the user is comfortable. The browser keyboard remains an option if microphone or MIDI access is unavailable.

For the user's own MusicXML, use “Open MusicXML” on the practice landing page instead of inventing a catalogue ID. Imported and scanned scores use temporary session storage; their local practice URLs are not shareable score links. Keep a downloaded copy when the user needs to retain the notation.

## Retrieve notation when requested

Resolve the returned `musicxml` URL against `https://tuneviva.com`. The download is compressed MusicXML (MXL), served as `application/vnd.recordare.musicxml`; save it as binary with an `.mxl` extension. It is not JSON or plain XML. Download once and reuse locally, honour cache headers, and consult the score page for licensing and attribution instead of assuming every arrangement is public domain.

This API is read-only. There is no server-side scan, upload or editing API. For the user's own photographed or PDF sheet music, direct them to `https://tuneviva.com/recognize`; recognition runs in their browser. MusicXML files can be opened from `https://tuneviva.com/learn/`.

## API references

- Documentation: https://tuneviva.com/docs/api
- OpenAPI specification: https://tuneviva.com/docs/api/openapi.json
- Health: https://tuneviva.com/api/practice/health (static export readiness only, not a guarantee that every download works)
