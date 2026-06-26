---
name: toon-json
description: Compress, encode, and decode large JSON payloads into a compact, reversible TOON string to reduce token usage in LLM prompts and tool payloads. Use when you need to shrink repeated JSON in prompts ("compress this JSON", "reduce token usage", "encode JSON"), transmit structured data cheaply, or round-trip JSON reliably (encode/decode/validate). Supports schema (key dictionary) mode for additional compression.
---

# toon-json (TOON v1)

Use the bundled script `scripts/toon_json.py` to encode JSON into a compact TOON string and decode it back losslessly.

## Commands

### Encode JSON -> TOON

- Minimal:

```bash
python3 scripts/toon_json.py encode < input.json
```

- With schema (better compression for repeated keys):

```bash
python3 scripts/toon_json.py encode --schema < input.json
```

- Pretty wrapper (includes schema metadata):

```bash
python3 scripts/toon_json.py encode --schema --pretty < input.json
```

### Decode TOON -> JSON

```bash
python3 scripts/toon_json.py decode < input.toon
```

### Derive a schema (key dictionary) from JSON

```bash
python3 scripts/toon_json.py schema < input.json
```

## Operational guidance

- Prefer `--schema` when:
  - The JSON has many repeated keys (APIs, config blobs, tool outputs)
  - You will send similar objects repeatedly across turns
- Prefer schema-less mode when:
  - One-shot payloads
  - You want maximum human readability

## Safety / correctness

- The format is designed to be lossless for JSON types: object, array, string, number, boolean, null.
- Rejects non-JSON numbers (NaN/Inf) and non-string object keys.
- If decoding fails, re-run with `--pretty` output on encode to inspect the embedded schema.
