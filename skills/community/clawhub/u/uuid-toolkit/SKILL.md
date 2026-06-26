---
name: uuid-toolkit
description: Generate, parse, validate, and convert UUIDs (v1/v3/v4/v5), ULIDs, and NanoIDs. Use when creating unique identifiers, parsing existing UUIDs to extract version/timestamp/node info, validating identifier formats, converting between UUID representations (hex, base64, URN, integer), or generating bulk IDs. No external dependencies.
---

# UUID Toolkit

Generate, parse, validate, and convert UUIDs, ULIDs, and NanoIDs. Zero dependencies (Python 3.9+).

## Quick Start

```bash
# Generate a UUIDv4
python3 scripts/uuid_toolkit.py generate uuid4

# Generate 10 ULIDs
python3 scripts/uuid_toolkit.py generate ulid --count 10

# Parse a UUID
python3 scripts/uuid_toolkit.py parse 550e8400-e29b-41d4-a716-446655440000
```

## Commands

### generate
Create identifiers of any type:
```bash
python3 scripts/uuid_toolkit.py generate uuid4                      # Random UUID
python3 scripts/uuid_toolkit.py generate uuid1                      # Time-based UUID
python3 scripts/uuid_toolkit.py generate uuid5 --name example.com   # Deterministic
python3 scripts/uuid_toolkit.py generate ulid                       # Sortable ULID
python3 scripts/uuid_toolkit.py generate nanoid --size 16           # Short NanoID
python3 scripts/uuid_toolkit.py generate uuid4 --count 100 --upper  # Bulk, uppercase
python3 scripts/uuid_toolkit.py generate nil                        # Nil UUID
```

Types: `uuid4`, `uuid1`, `uuid3`, `uuid5`, `ulid`, `nanoid`, `nil`.

### parse
Extract detailed info from an identifier:
```bash
python3 scripts/uuid_toolkit.py parse 550e8400-e29b-41d4-a716-446655440000
python3 scripts/uuid_toolkit.py parse 01ARYZ6S41T1ZTXYZ1234ABCDE  # ULID
```

Shows version, variant, timestamp (v1/ULID), node/MAC (v1), hex, integer.

### validate
Check if identifiers are valid:
```bash
python3 scripts/uuid_toolkit.py validate 550e8400-e29b-41d4-a716-446655440000 not-a-uuid
```

### convert
Convert UUID between representations:
```bash
python3 scripts/uuid_toolkit.py convert 550e8400-e29b-41d4-a716-446655440000
```

Outputs: standard, uppercase, no-dashes, URN, integer, base64, bytes-LE, braces.
