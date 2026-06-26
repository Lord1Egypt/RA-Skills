---
name: sqlite-turso-migration
version: 0.1.0
status: draft
description: >
  Prisma PostgreSQL → SQLite/Turso migration pattern for AI workspaces — converts
  production Postgres schemas to edge-compatible SQLite with Turso replication. Use when
  moving from a hosted Postgres database to a lightweight embedded SQLite setup, enabling
  local-first development with optional Turso cloud sync, or reducing database costs by
  replacing managed Postgres with Turso's generous free tier for low-traffic AI applications.
requires:
  env:
    - TURSO_DATABASE_URL
    - TURSO_AUTH_TOKEN
    - DATABASE_URL
  bins:
    - node
    - python3
metadata:
  openclaw:
    primaryEnv: TURSO_DATABASE_URL
    network:
      outbound: true
      reason: "Connects to Turso cloud for schema sync and optional replication."
    security_notes: "Draft skill — not yet published"
---

# SQLite/Turso Migration

> **STATUS: DRAFT** — This skill is planned but not yet fully implemented.

## What This Does

Provides a step-by-step migration pattern for moving Prisma-managed PostgreSQL schemas to
SQLite (local) or Turso (edge-replicated SQLite). Handles the key incompatibilities between
Postgres and SQLite: no arrays (→ JSON columns), no enums (→ text with check constraints),
no UUID type (→ text), and different auto-increment semantics. Includes a validation harness
to verify data integrity post-migration.

## Planned Capabilities

- Prisma schema converter: Postgres dialect → SQLite-compatible schema
- Data migration script with batched upserts and progress reporting
- Turso connection adapter for Prisma (via `@prisma/adapter-libsql`)
- Type mapping reference: Postgres → SQLite equivalents
- Rollback procedure with dual-write transition period
- Integration tests comparing query results across both databases

## When To Use

- Moving a low-traffic AI app from Supabase/Neon/Railway Postgres to Turso to cut costs
- Building local-first apps that sync to Turso for multi-device access
- Migrating from Drizzle/Prisma Postgres to a SQLite-compatible edge setup
- Reducing database cold-start latency by switching from hosted Postgres to embedded SQLite
