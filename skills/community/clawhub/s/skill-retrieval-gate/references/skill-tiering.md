# Skill Tiering

Use this file to decide how aggressively retrieval should be used.

## Tier A — Retrieval-first

Usually retrieve first for:

- coding and project work
- deployment, infra, config, and troubleshooting
- knowledge-base organization
- reviews, summaries, and follow-up work that depend on existing notes

Reason: these tasks often depend on local history and prior decisions.

## Tier B — Retrieval-optional

Retrieve only when the user or task implies prior context.

Typical examples:

- GitHub or issue / PR work
- operations work with possible history dependence
- document organization where local notes may or may not matter

## Tier C — Usually skip retrieval

Usually skip retrieval for:

- weather
- text-to-speech
- image generation
- simple message sending
- one-shot browser actions
- simple conversions or formatting tasks

Reason: retrieval often adds latency and noise without improving quality.
