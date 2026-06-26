# Troubleshooting

## `INSTALL_RUNTIME_REQUIRED`

Run:

```bash
bash skills/social-video-distill/scripts/install_runtime.sh
```

## No captions found

Possible causes:
- the platform does not expose subtitles
- the clip has no manual/auto captions
- the URL is geo/auth restricted

Next moves:
1. try browser AI distillation from any rough transcript or notes
2. download the media only if the task truly requires transcript recovery
3. use local ASR only as fallback

## Gemini CDP endpoint unreachable

Check:

```bash
curl -fsS http://127.0.0.1:9222/json/version
```

If unreachable, restore the debug Chrome session first.

## Gemini page loaded but input not found

The web UI may have changed.

Try:
1. confirm Gemini is already logged in in the debug browser
2. inspect current editable selectors
3. patch `scripts/ask_gemini_cdp.js`

## Gemini returns a weak answer

Usually the prompt is too broad.

Fix by narrowing the ask:
- summary only
- humor structure only
- caption options only
- quote extraction only
