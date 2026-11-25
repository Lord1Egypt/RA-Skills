---
spec: usk/3.0
id: sealed-chain-en
version: 1.0.0
skill_type: functional
name: Multi-Agent Cross-Device Encrypted Collaboration (Email + Task Sealing)
description: Functional skill. Coordinate multi-agent cross-device encrypted collaboration using MGC 1.6.0 chain mode. Split a workflow by data domain into N sealed sub-packages; each execution agent receives only the scripts authorized for it. Data and credentials never leave local storage; only task cards, scripts, and result summaries flow across devices. Default dispatch is email; task payloads travel as sealed sub-packages. Includes role-reference task-card templates, a credential-access example, and a task-flow template.
author: MirginCipher Team
license: MIT
tags: multi-node collaboration, chain mode, task-chain sealing, encrypted delivery, node authorization, zero-exposure, a2a, distribution index, automated dispatch, workflow splitting, orchestration, mgc, blackbox, functional
platform_compatibility: windows, macos, linux
mcp_tools: mgc_save, mgc_save_file, mgc_get, mgc_run, mgc_find, mgc_list, mgc_seal, mgc_seal_package, mgc_package, mgc_delete, mgc_open_webui, mgc_skill
requirements:
  mgc_version: ">=1.6.0"
install: pip install mgc-blackbox>=1.6.0
runtime: mgc
port: 57219
changelog:
  - version: 1.0.0
    changes:
      - Initial release based on MGC 1.6.0 chain mode
      - Three reference roles: orchestrator agent / internal execution agent / external execution agent (split by data domain)
      - Eight-stage collaboration protocol: prepare → author → store → seal → dispatch → execute → return → aggregate
      - Hard constraints: data and credentials never ship inside sub-packages, workflow directory must be flat, targets files must exactly match diff_3
      - Default email dispatch (Subject keyword chain:<task_id>, sha256 in body), with A2A / HTTPS / shared folder also supported
      - distribution_index.json drives automated dispatch; node fingerprint ledger matches each sub-package to recipient
      - UNSEAL_FAILED error code: import success does NOT guarantee unsealing — node_pub mismatch surfaces only at run time
      - Sealed script ext01 portability reminder (python vs python3), --output parent directory must exist beforehand
      - Script-wrapped encrypted transport: task cards and result summaries sealed inside .py files alongside scripts
      - Five role_prompts templates: orchestrator task card / dispatch instructions / executor task card / result return / orchestrator return receipt
      - Examples: role_prompts.md, use_credential.py (local MGC credential access), task_flow.md (fill-in template)
      - Targets specs contain .py only; data files and credentials stored locally by each executor
      - Clear boundary with single-device soft-isolation skill (task_chain_meta_skill)
      - Covers three-step delivery flow, three-node example, distribution_index.json, and @file long-spec form
      - Flat-directory hard constraint, text-file REST API reads, real naming and field references
---

# Skill scope

**Functional skill**: answers "how does chain mode work, how do multiple agents split roles, how do data and credentials stay local".

- **Covers**: mechanism, role model, collaboration protocol, hard constraints, API usage, templates, examples.
- **Does not cover**: industry- or business-specific splitting plans. Those belong to future scenario skills and are outside this skill's scope.

For: workflows that need splitting across multiple agents by data domain, where data and credentials must stay on local devices.

---

# One-liner

The orchestrator agent writes only task cards and scripts. MGC splits out N sealed sub-packages by data domain. Each execution agent receives only its own scripts. Data and credentials never leave local storage; only result summaries flow back.

---

# Role model

Three **reference roles**, not fixed headcount. Split is by **data domain**, not by device.

| Role | Count | Holds data / credentials | Responsibility | Output |
|------|------|:---:|----------------|--------|
| Orchestrator agent | 1 | ❌ | Split task, write task card, produce spec, dispatch, aggregate | Task card, targets spec, aggregate report |
| Internal execution agent | 1 per internal data domain | ✅ local only | Execute scripts inside the domain | Result summary |
| External execution agent | 1 per external data domain | ✅ local only | Execute scripts inside the domain | Result summary |

Splitting rules:

1. **Only one orchestrator agent**, which must not hold any business data or credentials.
2. **Execution agents are split by data domain**: at least one per domain, can be more.
3. Single-domain scenario = 1 orchestrator + 1 internal executor, no external executor.
4. "Internal / external" is a data boundary, not a hardware type; the same machine can host two data domains.

Task-card templates in [examples/role_prompts.md](./examples/role_prompts.md).

---

# Chain Mode mechanism

## One call → N sealed sub-packages

`mgc_seal_package` takes a target array in `ext04`. MGC produces an independent sub-package per target's `files`:

```json
[
  {"node_pub": "<internal executor PEM>", "files": ["analyze.py", "shared_helper.py"]},
  {"node_pub": "<external executor PEM>", "files": ["intel.py", "shared_helper.py"]}
]
```

Output:

```
chain_delivery/<info_owner>__<diff_2>/
├── README.md                         # Human-readable: node_pub map + warnings
├── distribution_index.json           # Machine-readable: sha256 + granted files
├── task_package_01/                  # Internal executor only (index starts at 1)
│   ├── <info_owner>__<diff_2>__01.mgc_file
│   └── README.md
└── task_package_02/                  # External executor only
    ├── <info_owner>__<diff_2>__02.mgc_file
    └── README.md
```

Each sub-package unseals only for its own `node_pub`. Packages cannot be cross-opened.

## Comparison with p2p / free mode

| | p2p mode | free mode | **chain mode** |
|---|---|---|---|
| `ext04` | single PEM | omitted | **target array** |
| Sub-packages | 1 | 1 | **N** |
| Can unseal | that PEM only | any 1.5.4+ | **each own PEM** |
| Best for | single-node auth | public distribution | **multi-agent collaboration** |
| distribution_index.json | ❌ | ❌ | ✅ |
| Producer version | 1.5.4 | 1.5.4 | **1.6.0** |
| Receiver version | 1.5.4 | 1.5.4 | 1.5.4 |

---

# Hard constraints

## Constraint 1: data and credentials never ship inside sub-packages

This is the core of the collaboration model and the fundamental difference between chain mode and simply "sending a folder".

| Item | Goes into sealed package? | Notes |
|------|:---:|-------|
| Scripts `.py` | ✅ | Encrypted by MGC |
| Task card prompt | ⚠️ see below | Only encrypted if wrapped as a script |
| Result summary | ⚠️ see below | Only encrypted if wrapped as a script |
| Data CSV / JSON | ❌ **forbidden** | Stored by the executor in local MGC |
| Credential token / key | ❌ **forbidden** | Stored by the executor in local MGC |

Correct flow:

```
Executor: data / credentials → store in [local MGC] (info_type=text) → never travel outward
Orchestrator: only publishes .py scripts
At run time: scripts read data / credentials via local MGC REST API → one-shot use
Return: only result summaries
```

Credential-reading example in [examples/use_credential.py](./examples/use_credential.py).

## Constraint 2: MGC only encrypts scripts

Chain mode encrypts executable scripts such as `.py` / `.sh`. CSV, JSON, TXT, and config files are **plaintext** inside the sub-package.

Corollaries:

- Putting data / credentials in the package = sending plaintext outbound. **Must be avoided**.
- If task cards and results must travel encrypted, they must be **wrapped as scripts** (see "Encrypted transport pattern").

## Constraint 3: workflow directory must be flat

MGC's sealed import hook supports flat imports only:

```python
from shared_helper import write_json   # ✅
from utils.shared_helper import ...    # ❌ ModuleNotFoundError
```

Therefore a workflow directory must not have `scripts/`, `utils/`, `data/`, or other sub-directories. All files live at the same level.

## Constraint 4: targets files = diff_3 at store time

`files` must exactly match the `diff_3` values recorded in MGC. Under a flat directory these are pure file names. Run `mgc_find` to verify before writing the spec.

## Constraint 5: sealed scripts return pid + status only

`mgc_run` on a sealed script returns `{"status": "started"}`. Results must be written out by the script (file / local MGC / return package).

Note: when passing `--output` through `ext02`, **create the parent directory first**. Sealed scripts do not auto-mkdir; a missing directory causes bootstrap code=1.

---

# Collaboration protocol

Eight stages. A fill-in version lives in [examples/task_flow.md](./examples/task_flow.md).

| Stage | Responsible role | Action | Output |
|-------|-----------------|--------|--------|
| 0 Prepare | Each executor | Store local data / credentials in local MGC | Local text records |
| 1 Author | Orchestrator | Write task card, prepare flat script directory | Task card + scripts |
| 2 Store | Orchestrator | `mgc_save_file` the script directory | Script records |
| 3 Seal | Orchestrator | Build targets (.py only) → `mgc_seal_package` | N sub-packages + index |
| 4 Dispatch | Orchestrator | Deliver sub-packages (default: email) | Delivery confirmation |
| 5 Execute | Each executor | Import → verify grant list → `mgc_run` | Result summary |
| 6 Return | Each executor | Wrap results → send back | Return package |
| 7 Aggregate | Orchestrator | Import return package → run and read → merge | Final deliverable |

"Verify grant list" is the key step against privilege escalation: after importing, the executor first calls `mgc_find` to confirm the actual files match the task card, and stops if they don't.

Stage 7 receiver-side actions (orchestrator view): receive return email → verify sha256 → `mgc_save_file` import the return package → `mgc_run` the return script to read the summary (see [examples/role_prompts.md](./examples/role_prompts.md) template 5).

---

# Orchestrator operations

## Step 1: store script directory

```python
mgc_save_file(
    path="./pipeline",          # flat directory, .py files only
    info_owner="<owner>",
    diff_2="pipeline",
)
```

MGC auto-parses argparse → ext02, scans imports → ext05, builds cross-script call graph → ext08, static checks → ext10.

> ⚠️ Before sealing, spot-check each script's **ext01** with `mgc_get`. MGC may infer `python` instead of `python3`. Some Linux distros only ship the `python3` alias, causing the sealed package to fail on the executor's machine. Confirm portability against the target executor's environment.

## Step 2: prepare target spec

Option A (short spec inline):

```python
targets = json.dumps([
    {"node_pub": "<internal executor PEM>", "files": ["analyze.py", "shared_helper.py"]},
    {"node_pub": "<external executor PEM>", "files": ["intel.py", "shared_helper.py"]},
])
```

Option B (long spec file, recommended):

```json
[
  {"node_pub": "<internal executor PEM>", "files": ["analyze.py", "shared_helper.py"]},
  {"node_pub": "<external executor PEM>", "files": ["intel.py", "shared_helper.py"]}
]
```

```python
mgc_seal_package(
    info_owner="<owner>",
    diff_2="pipeline",
    ext04="@/abs/path/chain_targets.json",
    output_dir="/abs/path/chain_delivery",
)
```

> `node_pub` is obtained by each executor running `mgc_get(info_type='__NODE_PUB__', info_owner='__NODE_PUB__')` on its own machine. Use the multi-line PEM as-is; do not collapse to a single line.

## Step 3: dispatch

Maintain a **node fingerprint ledger** (e.g. `agent_config.json`): each entry maps email + node_pub + node_pub_fingerprint (the fingerprint is generated by MGC during sealing and written into `distribution_index.json` — the orchestrator only needs to record and match it, never compute it).

Before dispatching, match one by one: the `node_pub_fingerprint` of each sub-package in `distribution_index.json` ↔ the fingerprint for that recipient in the ledger. Confirm "this package goes to the correct node".

Email convention (default):

- **Subject keyword**: always `chain:<task_id>`. Executors poll and filter on this keyword.
- **sha256 in body**: write each attachment's sha256 in the email body (not only in the file name) so the receiver can verify before importing.
- `.mgc_file` must travel as an attachment. Do not paste base64 into the body.

Read `distribution_index.json`, match recipients by `node_pub_fingerprint`, and send each `task_package_NN/` to the corresponding executor.

---

# Executor operations

## Step 1: import and verify

After receiving, confirm the attachment's sha256 matches the body text, then import:

```python
mgc_save_file(path="./task_package_01/<package_name>.mgc_file", info_owner="<owner inside package>", diff_2="pipeline")
mgc_find(info_owner="<owner inside package>", diff_2="pipeline")   # verify grant list
```

> Records inside the package carry their own info_owner / diff_2. The values passed at import time are used for validation. Subsequent `mgc_find` / `mgc_run` calls should use the values from inside the package.
>
> ⚠️ **Import success ≠ unsealable**. Unsealing happens at run time. If the sub-package's node_pub does not match this machine (wrong node) or the `.mgc_file` has been renamed, `mgc_run` will report `UNSEAL_FAILED`. After verifying the grant list, smoke-test the entry script with small parameters first.

## Step 2: execute

```python
mgc_run(
    info_type="script",
    info_owner="<owner inside package>",
    diff_2="pipeline",
    diff_3="analyze.py",
    ext02='["--owner", "local_data", "--output", "/path/result.json"]',
)
```

## Step 3: return

Wrap the result summary in `report.py` (see next section), seal it with the orchestrator's node_pub in p2p mode, and return.

---

# Encrypted transport pattern (script-wrapped)

MGC encrypts scripts only. So for task cards and results to travel encrypted, they must be wrapped as scripts:

| Item | Wrapping | Effect |
|------|----------|--------|
| Task card prompt | `task_card.py`, prompt as a string constant | Encrypted by MGC |
| Result summary | `report.py`, results as string constants | Encrypted by MGC |

Example `task_card.py`:

```python
TASK = """
Goal: ...
Constraints: ...
Deliverables: ...
"""

if __name__ == "__main__":
    print(TASK)
```

The task card now travels sealed alongside the scripts, never appearing as plaintext in the sub-package. Without wrapping, task cards must travel via external channels such as email body — verify whether the content is sensitive before choosing that path.

---

# Dispatch methods

| Method | Best for | Notes |
|--------|----------|-------|
| **Email attachment** | Cross-org, needs human confirmation and audit | **Default recommendation**: minimal dependency, leaves an audit trail. Subject uses `chain:<task_id>`, sha256 in body |
| Shared folder | Same-org intranet | Simplest |
| A2A message | Platforms with direct agent connectivity | Keep `.mgc_file` suffix; verify sha256 before import |
| HTTPS / object storage | Cross-region automation | Each party serves its own download link |

A2A rules: preserve `.mgc_file` suffix; verify sha256 before import; never embed keys in the message body; prefer links over raw files.

---

# examples directory

| File | Purpose |
|------|---------|
| [role_prompts.md](./examples/role_prompts.md) | Task-card templates for three roles plus dispatch and return — copy and use directly |
| [use_credential.py](./examples/use_credential.py) | Reads a credential from local MGC and uses it. No disk write, no print, outputs a summary only |
| [task_flow.md](./examples/task_flow.md) | Fill-in template for multi-agent task flows |

`use_credential.py` usage:

```bash
# Local debug
python3 examples/use_credential.py --local --token-file ./api_token.txt

# Sealed run (called by executor agent inside mgc_run)
# ext02='["--owner","local_credentials","--name","api_token.txt"]'
```

---

# Prerequisites

- **Python 3.10+** (1.6.0 tested on macOS Apple Silicon with framework-build Python 3.11; note sealed-package ext01 may be `python`, in which case the executor's environment must provide that alias — see orchestrator step 1)
- **MGC Blackbox ≥ 1.6.0** (producer); receivers ≥ 1.5.4
- `pip install mgc-blackbox`
- `mgc` running, API `http://127.0.0.1:57219`, WebUI `http://127.0.0.1:57218`

Hard limits: each sub-package ≤ 100 files and ≤ 50 MB (`TOO_MANY_FILES` / `PACKAGE_TOO_LARGE`).

---

# Error codes

| Code | Meaning | Action |
|------|---------|--------|
| `UNSEAL_FAILED` | Unseal failed: `Double-layer unseal failed: Incorrect decryption` | **Import success, failure only at run time**. Typical causes: sub-package sent to wrong node (node_pub mismatch), `.mgc_file` renamed and lost suffix, package metadata tampered. Check `distribution_index.json` fingerprint against this machine, confirm package ownership with orchestrator |
| `TOO_MANY_FILES` | Sub-package exceeds 100 files | Reduce granted files or seal in multiple passes |
| `PACKAGE_TOO_LARGE` | Sub-package exceeds 50 MB | Split large files and re-seal |
| `MISSING_REQUIRED_FIELDS` | `ext04` is not a valid array | Check JSON; use `@file` for long specs |
| `Invalid PEM format` | node_pub is not multi-line PEM | Copy as-is, preserve line breaks |
| `files not found in storage` | files do not match diff_3 | Run `mgc_find` to verify and correct |
| `FOLDER_CONTAINS_MGC_FILE` | Entire directory stuffed into one package for import | Import each `.mgc_file` individually |

---

# MCP tool cheat sheet

| Tool | Purpose | Required |
|------|---------|----------|
| `mgc_save_file` | Store script directory / import sub-package | path, info_owner |
| `mgc_seal_package` | Chain-mode seal | info_owner, diff_2, output_dir, ext04 |
| `mgc_find` | Verify diff_3 / grant list | info_owner |
| `mgc_run` | Execute sealed script | info_type="script", info_owner, diff_3 |
| `mgc_get` | Fetch node_pub | info_type="__NODE_PUB__" |
| `mgc_seal` | Single-package p2p return | info_owner, output_dir, ext04 |
| `mgc_list` | List metadata | — |
| `mgc_delete` | Delete entry | info_type, info_owner |
| `mgc_open_webui` | Open WebUI | — |

---

# Relationship with p2p / free mode

```
mgc_seal_package(ext04=single PEM)     → p2p mode (1 node)
mgc_seal_package(ext04=omitted)        → free mode (any node)
mgc_seal_package(ext04=target array)   → chain mode (N nodes)
```

Chain mode is the multi-node extension of p2p: each sub-package is independently sealed. Modes can be mixed — for example, use chain to dispatch core scripts, then p2p to seal result returns.

---

# Security boundary

MGC protects confidentiality and node binding:

- A sub-package unseals only for the node holding the matching private key
- Link authorization (`ext07` / `ext09`) — tampering causes unseal failure
- Run-time behavior of sealed scripts is the responsibility of the script author
- **Non-script files are plaintext inside sub-packages** — this is why data and credentials cannot go into a package, and why "data residency" is a hard requirement

---

# Related skills

- **MGC Blackbox meta-skill** — overview of p2p / free / chain modes
- **Sealed workflow skill** — p2p / free mode detailed guide
- Scenario skills (future) — splitting plans for specific business domains, depending on this skill

---

# Contact

- Main repo: https://github.com/zkeviny/MGC-Blackbox
- Issues: https://github.com/zkeviny/MGC-Blackbox/issues
- Email: mirgincipher@outlook.com
