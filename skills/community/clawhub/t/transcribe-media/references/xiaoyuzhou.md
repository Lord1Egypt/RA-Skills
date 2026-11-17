# Transcribe a Xiaoyuzhou Episode

Read this file only when processing a Xiaoyuzhou episode URL.

## Recognize the episode URL

Accept only a public episode URL matching
`https://www.xiaoyuzhoufm.com/episode/<24-character-id>` or the equivalent URL
without `www`. Reject podcast homepages, lists, live streams, and private or
paid episodes.

## Retrieve audio and run ASR

Xiaoyuzhou requires remote ASR. First make the external-processing disclosure in
the main `SKILL.md` and obtain the user's explicit approval. Then run:

```bash
node "{baseDir}/scripts/transcribe.mjs" --url "<complete Xiaoyuzhou episode URL>" --allow-remote-asr
```

The script skips caption extraction, retrieves the public episode audio through
the controlled media downloader, and then follows the AudioFlow authorization
workflow in the main `SKILL.md` before running ASR. Do not add the removed
`--xiaoyuzhou-mode` option.

If the command reports that managed `yt-dlp` is unavailable, obtain the separate
tool-download approval before rerunning with `--allow-tool-download` as well.

Never request a phone number, CAPTCHA result, SMS code, or Xiaoyuzhou account
credential. Do not call Xiaoyuzhou login, SMS verification, or official
transcript interfaces, and do not read or store Xiaoyuzhou account credentials.

## Handle the result

Treat the ASR result as an immutable raw transcript and follow the direct-output
rules in the main `SKILL.md`. After obtaining a result, do not download the audio
again or call AudioFlow again.
