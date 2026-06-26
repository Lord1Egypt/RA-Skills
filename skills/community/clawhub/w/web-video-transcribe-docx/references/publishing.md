# Publishing

## Release Checklist

1. Keep the skill folder name, frontmatter `name`, and release zip basename aligned.
2. Bump the version in `SKILL.md` metadata before each public release.
3. Re-run validation and at least one real extraction or transcription smoke test.
4. Keep the root `LICENSE` file and the `license` field in `SKILL.md` aligned. This release uses `MIT-0`.
5. If you have a public repository or homepage, add it to `metadata.openclaw.homepage` before publication.

## Marketplace Notes

### ClawHub / OpenClaw

- The listing benefits from `metadata.openclaw.requires` because the marketplace can surface runtime requirements.
- The broader Agent Skills spec also documents an optional `compatibility` field, but some older validators still reject it. This release keeps the runtime notes in the Markdown body to stay compatible with stricter legacy tooling.
- Keep `metadata` as a compact JSON object in frontmatter. This is easier for scanners and marketplace tooling to consume.
- This skill currently declares `python` or `python3` or `py` as acceptable runtime binaries because the scripts are Python-first.
- Browser extraction is optional. Do not mark Chrome or Edge as hard requirements at the metadata level because direct-media and local-file flows still work without a browser.

### Agent Skills ecosystem

- Keep frontmatter portable: `name` and `description` are the hard minimum; prefer conservative optional fields when you need to satisfy older validators.
- Avoid marketplace-specific instructions in the main workflow unless they materially help the agent use the skill.

## Suggested Tags

- transcription
- asr
- chinese
- docx
- video
- audio
- web-scraping
- toutiao

## Suggested Short Summary

Offline-first Chinese web media transcription skill that extracts playable audio or video from ordinary web pages, runs local SenseVoice ASR, and exports TXT plus DOCX deliverables.

## ClawHub Publish Template

Replace the placeholder values before running:

```powershell
clawhub skill publish `
  --slug web-video-transcribe-docx `
  --version 1.0.0 `
  --summary "Offline-first Chinese web media transcription skill with TXT and DOCX output." `
  --tags transcription,asr,chinese,docx,video,audio `
  --dir .
```

## Pre-Publish Smoke Tests

```powershell
python {baseDir}/scripts/bootstrap_env.py
python {baseDir}/scripts/extract_web_media.py --help
python {baseDir}/scripts/pipeline_web_to_docx.py --help
python {baseDir}/scripts/download_url.py --help
```

For a real smoke test, run either:

```powershell
python {baseDir}/scripts/pipeline_web_to_docx.py "https://example.com/video-page" --output-dir ".\out"
```

or:

```powershell
python {baseDir}/scripts/transcribe_sensevoice.py --input ".\sample.wav" --output-txt ".\out\transcript.txt" --output-docx ".\out\transcript.docx"
```
