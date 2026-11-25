---
spec: usk/3.0
id: sealed-audit-en
version: 1.0.0
name: Compliance Audit and Due-Diligence Review (Data Stays Home, Logic Stays Yours)
description: For investment due diligence, supplier audits, internal-control and data-compliance checks — the reviewer seals its checking logic into a package for the auditee, who runs it against its local database and returns only a summary. Data never leaves the auditee; the logic is never readable by the auditee. Built on MGC Blackbox 1.6.0 with a runnable minimal example.
author: MirginCipher Team
license: MIT
tags: audit, due-diligence, compliance, data-sovereignty, sealed-delivery, p2p, free-mode, mgc
platform_compatibility: windows, macos, linux
mcp_tools: mgc_save, mgc_save_file, mgc_get, mgc_run, mgc_find, mgc_list, mgc_seal_package, mgc_delete, mgc_open_webui, mgc_skill
requirements:
  mgc_version: ">=1.6.0"
install: pip install mgc-blackbox>=1.6.0
runtime: mgc
port: 57219
files:
  example_dir: examples/
changelog:
  - version: 1.0.0
    changes:
      - Initial release, built on MGC Blackbox 1.6.0
      - Covers p2p one-to-one audits and free-mode standard check packages
      - Ships a runnable minimal example — mock auditee database, checking rules, entry script, and task briefs for both sides
---

# Compliance Audit and Due-Diligence Review

## The pain in this scenario

Audits and due diligence require two disclosures that neither side wants to make:

- The auditee does not want to hand over its ledger, transaction records, or customer list;
- The reviewer does not want to hand over its checking logic, sampling rules, or risk model — otherwise the rules can be gamed or copied.

The traditional choice is binary: give data, or give logic. MGC removes the choice.

**Seal the checking scripts to the auditee → they run against the auditee's local database → only a summary comes back.**

## When to use it

- Investment due diligence: verifying a target company's ledger and revenue recognition
- Supplier audits: a core enterprise checking a supplier's qualification and settlement records
- Internal control and compliance: a group or external body checking a branch's business data
- Data-compliance self-checks: sending a standard package to auditees for self-assessment

## When it is not a fit

- The reviewer must inspect raw line items one by one → MGC protects against "handing over raw data", it does not deliver detail records
- The auditee has no environment that can run the scripts → Python 3.10+ and a local MGC are required
- Both sides already share one trust domain → use plain `mgc_package`, no sealing needed

## Two delivery modes

| | p2p one-to-one audit | free standard check package |
|---|---|---|
| How to seal | `ext04=auditee node_pub` | omit `ext04` |
| Who can run it | Only that auditee node | Any MGC 1.5.4+ node |
| Best for | A bespoke audit for one project | A general self-check package for many auditees |
| Key exchange | Required | Not required |

## The full audit chain

| Stage | Who | Action |
|---|---|---|
| 1. Prepare | Auditee | Confirm the local database is readable; store credentials in the local MGC if needed |
| 2. Fetch key | Auditee | `mgc_get(info_type="__NODE_PUB__", info_owner="__NODE_PUB__")` and send the public key to the reviewer (both `info_type` and `info_owner` **must** be `__NODE_PUB__`) |
| 3. Seal | Reviewer | `mgc_seal_package(..., ext04=auditee_pub, output_dir=...)` |
| 4. Deliver | Reviewer | Hand over the `.mgc_file` by email / shared drive, with the sha256 in the body |
| 5. Import | Auditee | `mgc_save_file(path="xxx.mgc_file", info_owner="audit_pack")` |
| 6. Run | Auditee | `mgc_run(info_type="script", info_owner="audit_pack", diff_2="examples", diff_3="run_audit.py")` |
| 7. Return | Auditee | Send back only the result summary produced by the script |
| 8. Review | Reviewer | Check the summary; if needed, seal a new sampling rule and repeat |

**Stage 7 is the crux of the chain**: what goes back is a summary, not detail. The script must never write raw rows into its output file.

## Four hard constraints

1. **Data never goes into the package.** No CSV / SQLite / DSN ships with the package; data stays local and credentials live in the data owner's local MGC (`info_type=text` / `token`), read at runtime. Non-script files inside a sealed package are plaintext.
2. **Flat directory.** Scripts saved into MGC must sit at the same `diff_2` level. No `scripts/`, `utils/` subdirectories; cross-script calls require the same `diff_2` (`DIFF2_MISMATCH`).
3. **Whole-folder seal, no file list.** p2p / free `mgc_seal_package` has **no `files` parameter** (`files` only exists inside chain-mode `ext04` array elements); the whole folder is sealed automatically, and `diff_3` is each file's relative path inside the package.
4. **Output must be written explicitly.** MGC does not create the parent directory of `--output`; the script must `mkdir(parents=True, exist_ok=True)` itself.

## Runnable minimal example

`examples/` is a closed loop you can run on a single machine:

| File | Purpose |
|---|---|
| `prepare_sample_db.py` | Generates a mock auditee database (demo only; in production point at the auditee's own DB) |
| `checks.py` | Checking rules: schema, required fields, negative amounts, duplicate invoice numbers |
| `run_audit.py` | Entry script, imports `checks` at the same level, writes `audit_result.json` |
| `role_prompts.md` | Task briefs for reviewer / auditee |

Run it locally first (no MGC, just to verify the logic):

```bash
python examples/prepare_sample_db.py /tmp/audit_demo/sample_ledger.db
python examples/run_audit.py --db /tmp/audit_demo/sample_ledger.db --output /tmp/audit_demo/audit_result.json
```

The sealed loop through MGC:

```python
# Reviewer: store examples/ as a workflow package
mgc_save_file(path="./examples", info_owner="audit_pack")

# Reviewer: seal it for the auditee (delete the ext04 line for free mode)
mgc_seal_package(
    info_owner="audit_pack",
    diff_2="examples",
    output_dir="/tmp/audit_demo/delivery",
    ext04=auditee_pub,
)

# Auditee: import, then run (argument passing follows the official schema from mgc_skill)
mgc_save_file(path="/tmp/audit_demo/delivery/examples_delivery/examples.mgc_file",
              info_owner="audit_pack")
mgc_run(info_type="script", info_owner="audit_pack",
        diff_2="examples", diff_3="run_audit.py")
```

> `prepare_sample_db.py` is demo-only. It is not part of a real delivery package; in production the auditee points at its own database.

> **Import note**: when importing a sealed package via `mgc_save_file`, the `info_owner` you pass applies to the **package group only**; every record inside keeps the owner recorded at seal time (the `INFO_OWNER_NOT_APPLIED` warning is advisory, not an error). After import, confirm with `mgc_find(info_owner="<the package's own owner>")` and use that value for all subsequent `mgc_run` calls — the 5+1 cross-script check requires caller and target to share the exact same `info_owner`, otherwise the call fails with `OWNER_MISMATCH`.

## MGC tools quick reference

| Tool | Purpose |
|---|---|
| `mgc_get` | Fetch the local node_pub (both `info_type` and `info_owner` must be `__NODE_PUB__`); read local credentials |
| `mgc_save_file` | Store a workflow folder / import a `.mgc_file` |
| `mgc_seal_package` | Seal an entire workflow folder for the auditee |
| `mgc_run` | Black-box execution, `diff_3` targets the entry script |
| `mgc_find` / `mgc_list` | Locate stored entries |
| `mgc_delete` | Clean up expired audit packages |
| `mgc_skill` | Look up official parameters and artifact layout |

## Common failures

| Symptom | Cause | Fix |
|---|---|---|
| Import succeeds but `UNSEAL_FAILED` at run time | The package was forwarded to a non-authorized node, or `node_pub` is malformed | Run on the authorized auditee node; verify `node_pub` when re-sealing |
| `AMBIGUOUS_SCRIPT` | Only `info_owner` + `diff_2` were given and multiple records match | Add `diff_3` to pin the entry script |
| `DIFF2_MISMATCH` | `diff_2` is not the directory name | Use `mgc_find` to confirm the real `diff_2` |
| `ModuleNotFoundError` on the auditee side | Scripts use subdirectories, or a third-party dependency is missing | Flatten to one level; ship a dependency list with the package |
| No result file produced | The `--output` parent directory does not exist | `mkdir(parents=True)` inside the script |

## Security boundary

- The reviewer gets: the summary, the auditee's `node_pub`
- The reviewer does not get: the auditee's raw data
- The auditee gets: a runnable package and its own execution result
- The auditee does not get: script source or rule logic

MGC protects **content confidentiality**. After unsealing, the script runs with the operator's permissions; what it reads and writes is still determined by the auditee's environment — so the auditee should verify the package source and `sha256` before running it.

## Contact

mirgincipher@outlook.com
