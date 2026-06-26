# redacta

Pseudonymise patient identifiers and PII in text — and restore them. A local,
dependency-free Python pattern engine.

```bash
pip install redacta
```

```python
from redacta import redact, reinstate

redacted, report, token_map = redact(
    "Dear patient, NHS Number: 943 476 5919, tel 0113 278 4532."
)
# redacted -> "Dear patient, NHS Number: [NHS_NUMBER_1], tel [PHONE_1]."

original = reinstate(redacted, token_map)
# original -> "Dear patient, NHS Number: 943 476 5919, tel 0113 278 4532."
```

## What it detects

Deterministic, checksum-validated patterns: NHS numbers (Modulus-11), UK National
Insurance numbers, dates of birth (keyword-anchored; appointment dates left
intact), UK postcodes, US SSNs and ZIP codes, hospital/MRN numbers, emails, and
phone numbers. Same value → same token; a `token_map` lets you reverse it.

**Scope:** this library is the deterministic layer only. Names, postal addresses
and identifying ages need contextual judgement and are **not** covered here — the
[Redacta agent skill](https://clawhub.ai/nickjlamb/redacta) and the
[MCP server](https://www.npmjs.com/package/redacta-mcp) add those via reasoning.
Stdlib only, no network calls; review output before sharing.

## CLI

```bash
redacta letter.txt                 # prints JSON: redacted_text, report, token_map
redacta letter.txt --text-only     # just the redacted text
redacta-reinstate redacted.txt --map token_map.json
```

## License

MIT-0 (MIT No Attribution). Built by
[PharmaTools.AI](https://www.pharmatools.ai/redacta).
