# Universal Domain Risk & Xuan-Ping Review (EN edition)

Enter any domain, get a red/amber/green 8-dimension read-only risk report (v1.2.1 adds read-only compliance-publicity evidence and region-first ICP judgment), plus a deterministic I-Ching "Xuan-Ping" hexagram Easter egg.

## Quick start

```bash
python3 scripts/scan_domain.py example.com > /tmp/scan.json
python3 scripts/divination.py example.com > /tmp/div.json
python3 scripts/gen_report.py /tmp/scan.json /tmp/div.json ./report.md
```

Requires: Python 3.8+, `requests`. No account, key, or login state needed - pure external black-box read-only evidence throughout.

## About the "Xuan-Ping" hexagram

This is a deterministic, reproducible entertainment feature: the domain is normalized, hashed with SHA256, and mapped onto the King Wen order of the 64 I-Ching hexagrams plus a moving line. The same domain always yields the same hexagram; nothing is random. `divination.py` keeps the original Chinese hexagram names alongside their standard English names and English hexagram texts as a cultural cross-reference; all report output and all user-facing text are in English. **It is never part of the conclusions and never a decision basis.**

## Boundaries

- No panel login, no credentials, no configuration changes.
- Risk hints only, no legal opinion; no inference of server physical location or filing obligation. A missing filing number is NOT flagged as a risk: judge the hosting region first (overseas hosting usually has no ICP obligation).
- Compliance items report page 'present / absent' facts only; absence != violation / no obligation.
- No market-value figure, no fabricated traffic; failed evidence always degrades to "pending".
- The hexagram is a pure Easter egg, not in the conclusions, not a decision basis.

## License

MIT
