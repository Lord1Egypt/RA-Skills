# Troubleshooting — Voice Input

## 0) Required dependency: local faster-whisper

This skill depends on a local transcription endpoint:
- `http://127.0.0.1:18790/transcribe`
- usually backed by `openclaw-transcribe.service`

Checks:
```bash
systemctl --user status openclaw-transcribe.service
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:18790/transcribe -X POST -H 'Content-Type: application/octet-stream' --data-binary 'x'
```

If this is down/missing, voice input will not produce text.

## 1) No mic button visible

Check that voice-input.js is injected:
```bash
grep 'voice-input.js' "$(npm -g root)/openclaw/dist/control-ui/index.html"
```

If missing, re-run `bash scripts/deploy.sh`.

## 2) No transcription result

Check local faster-whisper endpoint first. Also verify the HTTPS proxy is forwarding `/transcribe` requests.

## 3) HTTPS proxy not running

This skill requires `webchat-https-proxy` to be deployed. Check:
```bash
systemctl --user is-active openclaw-voice-https.service
```
