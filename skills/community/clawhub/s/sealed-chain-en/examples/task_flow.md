# Multi-Agent Task Flow Template

> Fill-in template. Replace `<>` with your scenario details to produce a chain-mode collaboration flow.
> Principle: **data and credentials never leave local storage; only task cards, scripts, and result summaries travel**.

## 1. Scenario definition

| Item | Fill in |
|------|---------|
| Task name | `<e.g. Q3 competitive analysis>` |
| Goal | `<one-line description of the final deliverable>` |
| Orchestrator | `<node name / agent name>` |
| Data domains | `<internal domain: ...>`, `<external domain: ...>` |
| Final deliverable | `<report / dataset / decision recommendation>` |

## 2. Roles and data domains

| Role | Data domain | Local data / credentials | Scripts received | Output |
|------|-------------|--------------------------|------------------|--------|
| Orchestrator agent | — | none | — | Task card + spec + aggregate |
| Internal execution agent | `<internal domain>` | `<local MGC owner: ...>` | `<a.py, helper.py>` | `<result summary>` |
| External execution agent | `<external domain>` | `<local MGC owner: ...>` | `<b.py, helper.py>` | `<result summary>` |

> If there is only one domain, delete the "External execution agent" row. Add more rows for more domains using the same pattern.

## 3. Stage flow

| Stage | Responsible role | Action | Output | Acceptance |
|-------|-----------------|--------|--------|------------|
| 0 Prepare | Each executor | Store its data / credentials in **local** MGC | Local text records | `mgc_find` shows the records |
| 1 Author | Orchestrator | Write task card (Template 1), prepare flat script directory | Task card + script directory | No sub-directories; no data files among scripts |
| 2 Store | Orchestrator | `mgc_save_file(path="<script directory>")` | Script records | `diff_3` matches the spec |
| 3 Seal | Orchestrator | Build targets (.py only) → `mgc_seal_package` | N sub-packages + `distribution_index.json` | Sub-package count = domain count; sha256 recorded |
| 4 Dispatch | Orchestrator | Default: email each `task_package_NN/` (Subject with keyword, sha256 in body) | Delivery confirmation | Each executor receives exactly its own package |
| 5 Execute | Each executor | Verify sha256 → import → verify grant list → smoke test → `mgc_run` | Result summary | Grant list matches task card; no UNSEAL_FAILED |
| 6 Return | Each executor | Return per Template 4 (recommended: wrap in `report.py` and seal) | Return package | No raw data inside |
| 7 Aggregate | Orchestrator | Verify source fingerprint → import return package → run and read → aggregate | Final deliverable | All domain results present |

## 4. File grant matrix

| File | Internal executor | External executor | Notes |
|------|:---:|:---:|-------|
| `<a.py>` | ✅ | ❌ | Internal domain main script |
| `<b.py>` | ❌ | ✅ | External domain main script |
| `<shared_helper.py>` | ✅ | ✅ | Shared across domains (chain-mode cross-package sharing demo) |
| `<report.py>` | ✅ | ✅ | Sealed result return (optional) |

> Data files and credentials **do not appear in this table** — they are never packaged.

## 5. Targets spec template

```json
[
  {
    "node_pub": "<internal executor PEM>",
    "files": ["<a.py>", "<shared_helper.py>"]
  },
  {
    "node_pub": "<external executor PEM>",
    "files": ["<b.py>", "<shared_helper.py>"]
  }
]
```

## 6. Dispatch and return

| Step | Default method | Alternatives |
|------|----------------|--------------|
| Dispatch | Email attachment (`task_package_NN/`) | Shared folder / A2A / HTTPS |
| Return | Wrap in `report.py` → p2p seal → email | Plaintext summary (non-sensitive results only) |

Email convention (applies to both dispatch and return):

- Subject always uses `chain:<task_id>` (return can use `chain:<task_id>:return`) so both ends can poll and filter by keyword.
- Each attachment's sha256 is written in the email body, verified by the receiver before import.
- `.mgc_file` always travels as an attachment, preserving its suffix.

## 7. Acceptance checklist

- [ ] `granted_files` in each sub-package are all `.py`
- [ ] Data / credentials live only in each executor's local MGC
- [ ] Each executor verified its grant list
- [ ] Each executor smoke-tested the entry script first (import success ≠ unsealable — guards against UNSEAL_FAILED)
- [ ] Email Subject contains the agreed keyword, attachment sha256 matches body
- [ ] Return content contains no raw data or credentials
- [ ] sha256 in `distribution_index.json` matches the actual package
- [ ] Orchestrator agent never touched plaintext data

## 8. Minimal example (single domain)

```text
Task: aggregate local sales data and produce a summary
Data domains: internal sales data (1)

0 Prepare: executor stores sales.csv in local MGC (owner=local_sales)
1 Author: orchestrator prepares analyze.py
2 Store: mgc_save_file(path="./pipeline")   # analyze.py only
3 Seal: targets = [{"node_pub":"<executor PEM>","files":["analyze.py"]}]
4 Dispatch: email task_package_01/
5 Execute: executor imports → verify list → mgc_run("analyze.py")
6 Return: result summary → wrap in report.py → p2p seal → return
7 Aggregate: orchestrator decrypts and merges
```
