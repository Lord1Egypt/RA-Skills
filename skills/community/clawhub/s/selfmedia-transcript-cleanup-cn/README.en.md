# Faithful Chinese Transcript Cleanup

Turn authorized Chinese transcript text into a readable, reviewable draft while preserving facts, intended meaning, speakers, and timestamps. The result includes a clean copy, an edit log, and explicit uncertainty markers. It does not transcribe audio, invent missing words, or turn opinions into marketing copy.

## Input and output

Provide original transcript text (up to 6,000 Chinese characters or roughly 20 minutes), optional speaker/timestamp markers, and a cleanup level. You receive a clean transcript, itemized changes, and items needing confirmation. With no supplied audio evidence, names and numbers remain unchanged or are flagged.

```bash
npx skills add xxjrq/selfmedia-transcript-cleanup-cn
```

See [the Chinese guide](README.md), [success fixture](fixtures/success.md), and [insufficient-evidence fixture](fixtures/failure.md).
