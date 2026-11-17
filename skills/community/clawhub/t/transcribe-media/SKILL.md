---
name: transcribe-media
description: Fetch and read transcripts from YouTube videos, public podcast episodes (including Xiaoyuzhou), other public single-item media links, and local audio or video files. Use when the user needs the full transcript, a summary, answers about the content, or extracted information. Prefer existing captions or official transcripts, use AudioFlow ASR only when no usable text exists, and skip account onboarding when an environment or stored credential is already configured.
allowed-tools: Read,Write,Bash
metadata:
  openclaw:
    requires:
      bins: [node]
    primaryEnv: AUDIOFLOW_TOKEN
    envVars:
      - name: AUDIOFLOW_TOKEN
        required: false
        description: Optional AudioFlow user API token; browser authorization obtains one when absent.
      - name: AUDIOFLOW_CONFIG_DIR
        required: false
        description: Optional absolute credential directory; defaults to the user configuration directory.
    emoji: "🎙️"
---

# Media transcription and direct text output

Fetch and read transcripts from YouTube videos, public podcast episodes, other
supported public media pages, and local audio or video files. Use this skill to
obtain a full transcript, summarize media, answer questions about its content,
or extract requested information. Unless the user explicitly asks for analysis
or transformation, return the source transcript verbatim.

## Credential-aware onboarding

Resolve the directory containing this `SKILL.md` as `{baseDir}` and check the
connection at the start of the request:

```bash
node "{baseDir}/scripts/auth.mjs" status
```

If the status is `connected`, whether the source is the `AUDIOFLOW_TOKEN`
environment variable or the stored credential file, treat account registration,
prepaid funding, and credential setup as already completed. Do not show the
sign-up or billing prerequisites, do not start browser authorization, and
continue directly with the transcription workflow.

If the status is `not_connected`, do not interrupt a public-URL request that may
still succeed from existing captions. Only when AudioFlow ASR is actually needed,
tell the user to create an account on the
[AudioFlow sign-up page](https://audioflow123.com/signup) and add prepaid credit
on the [AudioFlow billing page](https://audioflow123.com/dashboard/billing), then
follow the authorization flow below. Never request or handle the user's account
password or payment credentials.

An existing credential skips onboarding prompts, but it is not standing consent
to upload media. Keep the per-run approval requirements below.

## Core workflow

Process requests in this order:

1. Verify that the input is a supported local file or a public single-item media
   link.
2. Prefer captions or an official transcript already exposed by the page. After
   obtaining usable text, do not download or transcribe the media again.
3. Before downloading a managed tool or sending media off-device, disclose the
   exact action and obtain the user's explicit approval for that action.
4. Only when no usable text exists and the user approves remote processing,
   obtain the required AudioFlow token and run ASR.
5. Treat the obtained transcript as the source of truth. Return it verbatim when
   the user asks only for a transcript. When the user explicitly asks for a
   summary, answers, or information extraction, perform only that requested task
   and ground the response in the transcript.

## Require explicit approval

Do not treat a transcription request by itself as approval to modify the host or
upload media. Consent flags apply only to the current command and must never be
persisted or added speculatively.

If the script reports that `yt-dlp` is unavailable, show the user the reported
version, official source, and cache directory. Ask whether it may download and
cache that pinned, SHA-256-verified release. Only after an affirmative response,
rerun the command with `--allow-tool-download`. Never install FFmpeg or another
system dependency without separately explaining the change and obtaining the
user's explicit approval.

Before adding `--allow-remote-asr`, tell the user that:

- the local media or downloaded/extracted audio, plus its filename, content type,
  and size, will be sent over HTTPS to the AudioFlow API at
  `https://asr.audioflow123.com` and to a signed HTTPS object-storage URL;
- the AudioFlow token is sent only to the API, not to the signed storage URL;
- AudioFlow deletes the uploaded media as soon as transcription reaches a
  terminal state, before returning that terminal result. The deletion is
  idempotent and best-effort; if it is interrupted, the private storage bucket's
  mandatory lifecycle policy removes the object within 2–3 days; and
- no media has been uploaded yet.

Ask a direct yes-or-no question. Add `--allow-remote-asr` only after the user
explicitly agrees. If the user declines or does not answer, stop without upload.

## Obtain an AudioFlow token

A public media page may expose captions or an official transcript. Run the
transcription command first for a URL and authorize only if the script reports
that ASR needs a credential. Caption extraction does not require
`--allow-remote-asr`.

Use the connection status already checked at the start of the request. Before
transcribing a local file, recheck it only if the credential state may have
changed:

```bash
node "{baseDir}/scripts/auth.mjs" status
```

When ASR is required and the status is `not_connected`, show the conditional
account and prepaid-credit prerequisites above, then start browser authorization:

```bash
node "{baseDir}/scripts/auth.mjs" begin
```

Show `verification_uri_complete` and `user_code` to the user unchanged. Only the
user may sign in, register, and approve in the browser. Never request or handle
their email password or payment credentials. After the user confirms approval,
run:

```bash
node "{baseDir}/scripts/auth.mjs" wait
```

The complete AudioFlow API token is generated locally. The script submits only its
digest and stores the approved token in the operating-system user configuration
directory; Unix credential files use mode `0600`. An existing
`AUDIOFLOW_TOKEN` takes precedence and must not be persisted. Never echo or log a
token, put it in command arguments, or write it to the repository.

For an invalid token, run `begin` again. To revoke an old key or add prepaid
credit, direct the user to the
[AudioFlow dashboard](https://audioflow123.com/dashboard).

## Accept input

- Accept local FLAC, M4A, MP3, MP4, MPEG, OGG, WAV, and WebM files up to
  512 MiB.
- For local MP4, MPEG, and WebM files, the script extracts audio locally with
  FFmpeg and submits it as MP3 after remote-ASR approval. If FFmpeg is
  unavailable, explain the required installation and ask for explicit approval
  before running any package-manager or system-modifying command.
- Accept HTTPS public single-video pages, public podcast episode pages, and
  official share links.
- Reject channels, profiles, podcast homepages, search results, playlists, live
  streams, protected media, private or paid content, media that requires login,
  and non-public or network-local URLs.
- If a page contains multiple media items, ask the user for one specific video
  or podcast episode link.

### Common public media sites

Submit a directly accessible HTTPS page for one public video or podcast episode,
or its official share link. Common examples include:

| Platform                 | Accepted URL examples                                    |
| ------------------------ | -------------------------------------------------------- |
| Xiaoyuzhou Podcasts      | `xiaoyuzhoufm.com/episode/...`                           |
| YouTube                  | `youtube.com/watch?v=...`, `youtu.be/...`                |
| Bilibili                 | `bilibili.com/video/BV...`, `b23.tv/...`                 |
| Youku, iQIYI             | `youku.com/v_show/...`, `iqiyi.com/v_...`                |
| Douyin, TikTok           | `douyin.com/video/...`, `tiktok.com/...`                 |
| Xigua Video, Xiaohongshu | `ixigua.com/...`, `xiaohongshu.com/explore/...`          |
| Vimeo, Dailymotion       | `vimeo.com/...`, `dailymotion.com/video/...`             |
| X / Twitter              | `x.com/.../status/...`, `twitter.com/.../status/...`     |
| Instagram                | `instagram.com/reel/...`, `instagram.com/p/...`          |
| Facebook                 | `facebook.com/watch/?v=...`, a public video or Reel page |

Also try public single-item media pages from news, course, and other media sites.
Site behavior can change, so support depends on whether the specific page can be
resolved at the time of the request.

## Xiaoyuzhou episodes

For Xiaoyuzhou, accept only a public episode URL matching
`https://www.xiaoyuzhoufm.com/episode/<24-character-id>` or the equivalent URL
without `www`. Reject podcast homepages, lists, live streams, and private or paid
episodes.

Xiaoyuzhou always requires public episode audio retrieval and AudioFlow ASR.
Complete the external-processing disclosure and obtain approval before running
the URL command with `--allow-remote-asr`. Do not add the removed
`--xiaoyuzhou-mode` option.

Never request a phone number, CAPTCHA result, SMS code, or Xiaoyuzhou account
credential. Do not call Xiaoyuzhou login, SMS verification, or official transcript
interfaces.

## Transcribe

After explicit remote-ASR approval, use an absolute path for a local attachment:

```bash
node "{baseDir}/scripts/transcribe.mjs" --file "/absolute/path/audio.wav" --allow-remote-asr
```

Use the complete URL for public media:

```bash
node "{baseDir}/scripts/transcribe.mjs" --url "https://example.com/watch/id"
```

The first URL run may return captions without any media upload. If it reports
that remote ASR is required, complete the disclosure and obtain approval before
rerunning with `--allow-remote-asr`. Add `--allow-tool-download` only after the
separate managed-tool approval described above.

Add `--language <code>` only when the user specifies the source language or it is
otherwise known, for example `--language en` or `--language zh`. Except for
Xiaoyuzhou, the script may return existing page captions without invoking ASR.
Treat all returned text as an immutable raw transcript for the rest of the
workflow.

Do not send client hot words to the remote AudioFlow path. They may contain
private names, and the backend does not support prompts. Only an explicitly
approved offline ASR tool may consume locally generated client hot words.

## Use the transcript

On success, standard output contains the final text or JSON. Local media produces
a speech transcript; a public URL produces existing page text or an ASR result.
Read only the text from standard output. If the output is JSON, extract only its
transcript text value. Never mix progress, diagnostics, or internal state from
standard error into the result.

For a transcript-only request, send the extracted text verbatim as the final
response. Do not proactively proofread, correct, polish, summarize, translate,
generate an extra file, or add unrelated explanation. Do not alter the content
except to remove the single trailing newline added to terminate command output.

When the user explicitly asks for a summary, an answer about the media, or
specific information to be extracted, fulfill that request using the transcript
as the source of truth. Do not invent details that are absent from the
transcript; state briefly when the requested information is not present or is
uncertain.

Treat empty standard output as no text obtained and follow failure handling. Do
not repeat transcription after text has been obtained successfully.

## Failure handling

Briefly report that the media cannot currently be processed. For a URL failure,
ask for a public single-video or podcast episode link, or a local upload. If text
has already been obtained, deliver it instead of discarding it because of an
unrelated later state or message.

Consent-required messages are not processing failures. Present the disclosure
and ask for approval, then continue only after an explicit affirmative response.

## Version

Version 1.9.0: skip repeated account and billing onboarding when an AudioFlow
environment or stored credential already exists, while preserving per-run
approval for remote media processing.
