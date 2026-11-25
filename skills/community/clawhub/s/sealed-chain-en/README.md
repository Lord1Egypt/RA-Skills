# Multi-Agent Cross-Device Encrypted Collaboration — Email + Task Sealing (Functional Skill)

> **v1.0.0** · MGC 1.6.0 · Functional Skill
> Split a workflow by data domain into N sealed sub-packages. Each execution agent receives only its authorized scripts. Data and credentials stay local; only task cards, scripts, and result summaries travel. Default transport: email.

## What this skill solves

Two common pain points when multiple agents collaborate across devices:

1. **File isolation** — you don't want every agent to receive every script.
2. **Data residency** — business data and credentials should never leave local storage.

Chain mode handles this: the orchestrator agent publishes scripts only. Each execution agent receives a sealed sub-package containing exactly the scripts authorized for its domain. Data and credentials stay in each executor's **local MGC**; scripts read them on demand via REST API.

## Roles

| Role | Count | Holds data / credentials |
|------|------|:---:|
| Orchestrator agent | 1 | ❌ |
| Internal execution agent | 1 per internal data domain | ✅ local only |
| External execution agent | 1 per external data domain | ✅ local only |

Roles are assigned by **data domain**, not by device. A single-domain scenario can run with just "1 orchestrator + 1 internal executor".

## Quick flow

```text
0 Prepare   Each execution agent stores its data / credentials in local MGC
1 Author    Orchestrator writes task card + prepares flat script directory
2 Store     mgc_save_file(path="./pipeline")
3 Seal      mgc_seal_package(ext04=targets)  → N sub-packages + distribution_index.json
4 Dispatch  Default: email each task_package_NN/
5 Execute   Executor imports → verifies grant list → mgc_run
6 Return    Result summary → sealed return package
7 Aggregate Orchestrator decrypts and merges
```

## Hard constraints

- **Data / credentials never ship inside sub-packages**: MGC only encrypts scripts. CSV / JSON / config files are plaintext in the package.
- **Workflow directory must be flat**: the sealed import hook does not support sub-directories.
- **`files` = `diff_3` at store time**: run `mgc_find` to verify before authoring targets.
- **Sealed scripts only return status**: results must be written out by the script itself; the parent directory for `--output` must exist beforehand (sealed scripts do not auto-mkdir).
- **Import success ≠ unsealable**: `UNSEAL_FAILED` surfaces at run time when `node_pub` mismatches. Smoke-test the entry script after verifying the grant list.

## examples

| File | Purpose |
|------|---------|
| `examples/role_prompts.md` | Task-card templates for the three roles plus dispatch and return |
| `examples/use_credential.py` | Read a credential from local MGC and use it — no disk write, no print |
| `examples/task_flow.md` | Fill-in template for multi-agent task flows |

## Prerequisites

- MGC Blackbox ≥ 1.6.0 (receivers ≥ 1.5.4)
- Python 3.10+
- `pip install mgc-blackbox` → `mgc` running (API `http://127.0.0.1:57219`)

## Full documentation

Mechanics, protocol, and error codes live in [SKILL.md](./SKILL.md).

## Links

- GitHub: https://github.com/zkeviny/MGC-Blackbox
- Issues: https://github.com/zkeviny/MGC-Blackbox/issues
- Contact: mirgincipher@outlook.com
