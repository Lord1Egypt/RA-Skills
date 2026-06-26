# Ingest and Sync Plan

## Modes

### 1. Initial seed
Goal:
- populate the local store with the core SherpaDesk entities needed for analysis

Expected first targets:
- accounts / clients ✅
- users / contacts ✅
- technicians ✅
- tickets ✅
- ticket comments / notes / relevant history ⏳

### 2. Ongoing delta sync
Goal:
- keep the local store current with minimal API load

Expected approach:
- track per-entity sync state locally
- prefer modified/updated timestamps where supported
- fall back to tiered recency rescans when the API does not offer reliable server-side dirty filtering
- use idempotent upserts
- record ingest runs and sync state locally

Current direction:
- hot open-ticket rescans for ~5-minute freshness
- keep a local open-ticket ID set updated from the hot lane
- warm closed-ticket rescans every few hours for items closed within the last 7 days
- cold historical audit slices daily/weekly

## Principles

- correctness over cleverness
- low request volume over aggressive freshness
- explicit cursor/watermark state over inferred magic
- preserve source timestamps and raw JSON where useful
- make analytical queries easy even if the source API is painful
- shape the canonical data so downstream retrieval/indexing for OpenClaw is straightforward

## Rate-limit / fragility policy

SherpaDesk API usage should be conservative by default.

Recommended discipline:
- serialize initial implementation work until real endpoint behavior is confirmed
- avoid large request bursts
- prefer small page sizes when endpoint behavior is uncertain
- use retry with backoff for transient failures
- cache known dimensions locally
- perform delta syncs against the narrowest viable entity set
- treat the documented `600 requests/hour` limit as real and leave safety margin below it
- default to deliberate pacing (roughly one request every 8+ seconds) until live behavior proves a faster safe envelope

## Watcher principle

The watcher should focus on **new tickets only** for the first implementation.
Do not attempt to solve every notification use case at once.
