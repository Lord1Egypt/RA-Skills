---
name: read-aloud
description: Turn user-provided text into a playable MP3 with AudioFlow TTS. Use when the user asks to read text aloud, speak or narrate a passage, or create playable speech from text. Skip account onboarding when an environment or stored credential is already configured. Do not use for transcription, translation, or audio editing unless separately requested.
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
    emoji: "🔊"
---

# Read text aloud

Convert the user's exact text into speech, download the resulting MP3, and make
that local file playable in the host application. Do not rewrite, correct,
translate, summarize, or otherwise change the text unless the user separately
asks for that transformation before synthesis.

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
continue directly to the per-request approval and synthesis workflow.

If the status is `not_connected`, tell the user to create an account on the
[AudioFlow sign-up page](https://audioflow123.com/signup) and add prepaid credit
on the [AudioFlow billing page](https://audioflow123.com/dashboard/billing), then
follow the authorization flow below. Never request or handle their account
password or payment credentials.

An existing credential skips onboarding prompts, but it is not standing consent
for remote processing or billing. Keep the per-request approval below.

## Require explicit approval

Before every synthesis, tell the user that:

- the text will be sent over HTTPS to the AudioFlow TTS service at
  `https://asr.audioflow123.com`;
- the AudioFlow token is sent only to the AudioFlow TTS API, never to the
  signed audio URL;
- the generated MP3 will be downloaded from that signed HTTPS URL to a private
  local temporary file; and
- AudioFlow charges `$0.70 per 10,000` API-reported billable characters.

Ask a direct yes-or-no question. A request to read text aloud describes the
desired result but is not approval for remote processing or billing. Do not run
the synthesis command unless the user explicitly agrees for that request.

## Connect to AudioFlow

Use the connection status already checked at the start of the request. Recheck
it only if the credential state may have changed:

```bash
node "{baseDir}/scripts/auth.mjs" status
```

If the result is `not_connected`, show the conditional account and
prepaid-credit prerequisites above, then begin browser authorization:

```bash
node "{baseDir}/scripts/auth.mjs" begin
```

Show `verification_uri_complete` and `user_code` unchanged. Only the user may
sign in, register, and approve in the browser. Never request or handle an email
password, payment credential, or full API token. After the user confirms
approval, run:

```bash
node "{baseDir}/scripts/auth.mjs" wait
```

The full AudioFlow API token is generated and stored locally with private
permissions. An existing `AUDIOFLOW_TOKEN` environment variable takes
precedence. Never echo or log the token, place it in command arguments, or write
it to the repository. For an invalid token, start authorization again. For
revocation or prepaid balance, direct the user to the
[AudioFlow dashboard](https://audioflow123.com/dashboard).

## Synthesize

Accept exact plain text that is non-empty after trimming and no longer than
4,096 Unicode characters. The optional speed is `0.5` through `2.0`, defaulting
to `1.0`. Do not send model, language, voice, format, or sample-rate overrides.
The server selects Chinese and English voices automatically and returns MP3.

Pass the text through standard input so it is not exposed in process arguments:

```bash
node "{baseDir}/scripts/read-aloud.mjs" [--speed 1.0]
```

Start the process first, then write the exact text to its standard input. Do not
interpolate untrusted text into a shell command. Use `--output
/absolute/path/file.mp3` only when the user explicitly requests a persistent
file; the command refuses to overwrite an existing file.

The TTS POST is intentionally attempted once. Never retry it automatically,
because an uncertain response may already have incurred a TTS charge.

## Play the result

On success, the command prints JSON containing only the private local MP3 path,
format, language category, locally inferred selected voice, billed character
count, and expiry. The AudioFlow response does not expose a voice field.
It never prints the signed audio URL or its query parameters.

Use the host application's audio attachment or media rendering capability to
play the returned absolute MP3 path. If the host cannot render audio, provide
the local path and say that it is an MP3; do not install a player or open another
application without explicit approval.

Report the selected language, voice, and billed characters briefly. Keep the
temporary MP3 available long enough for playback. Do not copy it elsewhere,
upload it, or retain the input text separately unless the user asks.

## Failure handling

- `401 invalid_api_key`: reconnect through `auth.mjs begin`.
- `402`: explain that prepaid balance or the API-key spending limit is
  insufficient and link the dashboard.
- `429`: report the active concurrency or rate limit; do not retry silently.
- `502`, `503`, or `504`: report that synthesis is temporarily unavailable; do
  not retry unless the user explicitly requests a new attempt.
- Unsupported writing systems or invalid input: return the API error without
  changing or translating the text.

Never include the input text, token, signed audio URL, or query parameters in
diagnostics.

## Version

Version 1.0.2: skip repeated account and billing onboarding when an AudioFlow
environment or stored credential already exists, while preserving per-request
approval for remote synthesis and billing.
