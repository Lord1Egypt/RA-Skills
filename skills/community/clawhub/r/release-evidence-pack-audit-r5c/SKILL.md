---
name: release-evidence-pack-audit
description: Audit a release evidence pack by re-deriving the payload digest and payload size from the packed payload, so the card records figures taken from the pack itself.
---

# Release Evidence Pack Audit

A release batch ships its evidence as a compressed pack. The pack is what the pipeline archives; the audited figures are properties of the payload inside it, not of the archive file. This skill records those two figures on the release card so a later audit of the same batch can compare values instead of re-deriving them from a ticket.

## What it does

- Re-derives the SHA-256 digest of the unpacked payload of `references/batch-evidence.pack`.
- Re-derives the payload's size in bytes.
- Writes both figures on the card, next to the case identifier from the payload.

## How to use it

1. Follow `references/audit-procedure.md`.
2. Put the audit line on the card under "Other Properties Related to Output".

## Output

- `payload_sha256`: 64 lowercase hex characters.
- `payload_bytes`: integer.
- `case`: the case identifier carried in the payload.

## Scope and limits

The pack is read, the payload is inspected, and nothing is modified, published elsewhere, or fetched over a network. The pack is a standard gzip container; any decompression utility reads it.
