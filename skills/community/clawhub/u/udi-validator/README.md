# udi-validator

Medical device UDI (Unique Device Identification) validator — an Agent Skill for
[MABS-compatible](https://agentskills.io) agent frameworks (Anthropic Agent Skills protocol,
MS-Agent, Claude Code, Qoder, CodeBuddy …).

## What it does

- Detects the issuing agency of a UDI string: **GS1 / HIBCC / ICCBBA (ISBT 128)**
- Fully parses **GS1 element strings** (the dominant UDI issuing agency for medical devices):
  25+ Application Identifiers incl. `01` GTIN, `10` lot, `11/17` dates, `21` serial …
- Verifies **GS1 GTIN mod-10 check digits**
- Validates date fields (YYMMDD), warns on expired expiry dates, supports GS1 "day unknown" (`DD=00`)
- Handles raw barcode output with FNC1 / group separators (ASCII 29)
- Computes GTIN-14 check digits

## Quick start

```bash
python scripts/udi_validate.py "0104006381333931" "0104006381333931 17 261031 10 AB1234"
python scripts/udi_validate.py --checkdigit 0400638133393
```

Full AI table and output conventions: see [SKILL.md](SKILL.md).

## Scope & honesty

Structural validation only. HIBCC check-character arithmetic and ICCBBA identity
verification are intentionally out of scope (detected, not validated). Database existence
checks (NMPA UDI 数据库 / FDA GUDID / EUDAMED) require online queries.

## License

MIT
