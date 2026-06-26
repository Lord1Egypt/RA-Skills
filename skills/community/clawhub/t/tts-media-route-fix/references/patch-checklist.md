# TTS media-route patch checklist

Use this checklist during patch + verification.

## Route behavior

- [ ] `GET /media/tts/<id>.mp3` exists
- [ ] `HEAD /media/tts/<id>.mp3` exists
- [ ] Methods other than GET/HEAD return `405`
- [ ] Missing/nonexistent id returns `404`
- [ ] Invalid range returns `416`

## Security

- [ ] Bearer auth required (same as gateway token policy)
- [ ] Filename/id validation blocks traversal and malformed names

## Output correctness

- [ ] `Content-Type: audio/mpeg`
- [ ] `Accept-Ranges: bytes`
- [ ] Range request returns `206` with partial bytes (or `200` if server policy)
- [ ] Response body is binary MP3, not HTML/Control UI

## tts.convert payload

- [ ] Returns `ok: true`
- [ ] Payload has `audioUrl: /media/tts/<id>.mp3`
- [ ] Payload has `mimeType: audio/mpeg`
- [ ] Payload has `format: mp3`

## Lifecycle

- [ ] TTS temp files TTL = 2–5 minutes
- [ ] Auto cleanup removes expired files

## Safety

- [ ] Every edited `gateway-cli-*.js` has `.bak`
- [ ] Gateway restarted after patch
- [ ] curl verification with Bearer + `--range 0-127` passes
