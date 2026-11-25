# Compliance Audit and Due-Diligence Review

> **Version 1.0.0** · Requires MGC Blackbox ≥ 1.6.0

The reviewer supplies the checking logic, the auditee supplies only the conclusion — data never leaves the auditee, and the logic is never readable by the auditee.

## Use cases

- Ledger and revenue verification in investment due diligence
- Supplier qualification and settlement-record audits
- Group internal control and branch compliance checks
- Standardized self-check packages for many auditees

## Install

```bash
pip install mgc-blackbox>=1.6.0
mgc
```

API `127.0.0.1:57219` / WebUI `127.0.0.1:57218`.

## Quick start

```bash
# 1. Build a mock auditee database (local demo only)
python examples/prepare_sample_db.py /tmp/audit_demo/sample_ledger.db

# 2. Verify the logic without MGC first
python examples/run_audit.py --db /tmp/audit_demo/sample_ledger.db \
                             --output /tmp/audit_demo/audit_result.json
```

Through MGC sealing:

```python
mgc_save_file(path="./examples", info_owner="audit_pack")
mgc_seal_package(
    info_owner="audit_pack",
    diff_2="examples",
    output_dir="/tmp/audit_demo/delivery",
    ext04=auditee_pub,          # delete this line for free mode
)
```

The auditee imports the package, runs it, and returns only `audit_result.json`.

## Layout

```
sealed-audit-en/
├── SKILL.md
├── manifest.json
├── README.md
└── examples/
    ├── prepare_sample_db.py   # mock auditee DB (demo only)
    ├── checks.py              # checking rules
    ├── run_audit.py           # entry script
    └── role_prompts.md        # reviewer / auditee task briefs
```

## Two delivery modes

| | p2p one-to-one | free standard package |
|---|---|---|
| Seal | `ext04=auditee node_pub` | omit `ext04` |
| Who can run it | Only that auditee node | Any MGC 1.5.4+ node |
| Best for | Bespoke audits | General self-checks |

## Three things to remember

1. **Data never goes into the package** — the auditee's database stays local, credentials live in its local MGC.
2. **Return only the summary** — no detail records in the output file.
3. **Verify sha256** — the auditee should confirm the package source before running it.

## Security boundary

MGC protects content confidentiality; it does not change the script's runtime permissions. Once unsealed, the script can still read/write files and reach the network under the operator's account — verify the source before running.

## Contact

mirgincipher@outlook.com
