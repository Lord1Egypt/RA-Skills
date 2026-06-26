---
name: uuid-tool
description: Generate universally unique identifiers (UUIDs) in versions v1, v4, v5, v7, and nil format, with bulk generation and namespace-based deterministic IDs.
---

# UUID Tool — Universal Unique Identifier Generator

Generate, parse, and inspect UUIDs across multiple standards. Supports time-based (v1, v7), random (v4), and namespace-based (v5) UUIDs for distributed systems, database keys, and idempotency tokens.

## Quick Start

```bash
# Generate a random UUID (v4)
uuid-tool --generate v4

# Generate a time-ordered UUID (v7, good for DB indexing)
uuid-tool --generate v7

# Generate 10 UUIDs at once
uuid-tool --generate v4 --count 10
```

## Usage

```bash
uuid-tool [COMMAND] [OPTIONS]

Commands:
  --generate VERSION   Generate UUIDs (v1, v4, v5, v7)
  --parse UUID         Parse and inspect a UUID string
  --nil                Generate the nil UUID (00000000-...)
  --from-name TEXT     Deterministic UUID v5 from namespace + name

Options:
  --count N            Number of UUIDs to generate (default: 1)
  --namespace NS       Namespace for v5: "dns", "url", "oid", "x500", or custom
  --upper              Output uppercase hex
  --no-hyphens         Remove dashes from output
  --json               Output as JSON array
```

## Examples

```bash
# Time-based UUID v1
uuid-tool --generate v1

# Time-ordered UUID v7 (good for DB primary keys)
uuid-tool --generate v7

# Deterministic UUID from a domain name
uuid-tool --from-name "example.com" --namespace dns

# Parse and inspect
uuid-tool --parse "550e8400-e29b-41d4-a716-446655440000"

# Batch generate 100 UUIDs in compact format
uuid-tool --generate v4 --count 100 --no-hyphens
```

## Features

- **4 UUID versions:** v1 (time), v4 (random), v5 (SHA-1 namespace), v7 (time-ordered)
- **Bulk generation:** Up to 1000 UUIDs in one call
- **Deterministic v5:** Same namespace + name → same UUID every time
- **Parse & decode:** Extract timestamp, version, variant from any UUID
- **Compact mode:** Remove dashes for space-constrained usage
- **JSON output:** Easy integration with scripts and APIs
- **Nil UUID:** Generate or validate against the all-zero nil UUID
