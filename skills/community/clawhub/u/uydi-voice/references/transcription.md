# Transcribe a local recording

Use Message for a voice message of up to 60 seconds. Use File for recordings up to 30 minutes, including interviews and meetings. Both accept a 16 kHz mono PCM16 WAV. The Skill can also extract and convert other local media if ffmpeg is installed.

Run these commands from the installed Skill folder. The model catalog shows availability and current rates. The quote uploads the recording, verifies the duration on the server and returns an exact credit amount. Creating a quote is free.

```sh
node scripts/uydi.mjs asr-models
node scripts/uydi.mjs asr-quote --model file --file ./interview.m4a
```

Message costs one credit per started five seconds. File costs one credit per started twenty seconds. For example, a 60-second recording costs 12 credits with Message or 3 with File. Use the quoted amount for the selected recording.

Before submitting, save the quote ID, its credit amount and a unique retry key. The following example uses a quote of 3 credits. Quotes expire after 15 minutes. The key must be saved before the first request so a retry can recover the same job.

```sh
KEY="$(node -p 'require("node:crypto").randomUUID()')"
node scripts/uydi.mjs asr-submit QUOTE_ID --quoted-credits 3 --key "$KEY"
node scripts/uydi.mjs asr-status TRANSCRIPTION_ID --wait
node scripts/uydi.mjs asr-history
```

After a connection failure, repeat asr-submit with the same quote, amount and key. After receiving a job ID, poll asr-status instead. A completed result contains text and any timed segments, with startMs and endMs in milliseconds. Failed jobs report an error and refund the charge. The Skill’s browser sign-in works for transcription. When using a personal token via MCP or the API, request transcription:write to quote and submit, and transcription:read for the catalog, status and history.
