---
spec: usk/3.0
id: sealed-delivery-en
version: 1.0.0
name: Analytics and Algorithm Delivery (Public Trial, Node-Licensed Production)
description: Productized delivery for independent analysts, algorithm vendors and small teams — free mode produces a trial package anyone can run, p2p mode produces a production package bound to one customer node. The customer runs it locally, data never leaves their database, and the vendor's source is unreadable. Built on MGC Blackbox 1.6.0 with a runnable minimal example.
author: MirginCipher Team
license: MIT
tags: algorithm-delivery, script-sales, trial-version, node-licensing, private-deployment, sealed-delivery, free-mode, p2p, mgc
platform_compatibility: windows, macos, linux
mcp_tools: mgc_save, mgc_save_file, mgc_get, mgc_run, mgc_find, mgc_list, mgc_seal_package, mgc_package, mgc_delete, mgc_open_webui, mgc_skill
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
      - Covers free trial packages and p2p node-licensed packages
      - Ships a runnable minimal example — sample data, forecast logic, entry script, and briefs plus licensing terms for both sides
---

# Analytics and Algorithm Delivery

## The pain in this scenario

Selling an analytics model or algorithm script usually hits three walls:

- The customer will not hand over data and only accepts on-premise deployment;
- You will not hand over source code, otherwise one delivery becomes permanent distribution;
- Trial and production versions need separate handling, and renewals or upgrades need re-issuing.

MGC's two sealing modes map directly to those two commercial stages: **free for the trial, p2p for the production license**.

## When to use it

- An independent analyst delivering forecasting, scoring, or cleaning models
- An algorithm vendor deploying on-premise, licensed per customer node
- A small team productizing an internal tool — trial first, production later
- Delivering scripts that must be "runnable, unreadable, non-resellable"

## When it is not a fit

- The deliverable is pure data or a report → MGC encrypts scripts, not data
- The customer refuses to install a local runtime → MGC is required: builder 1.6.0+, runner 1.5.4+; cross-script calls need 1.5.2+
- You need online metering or billing → that is SaaS, not local delivery

## Two delivery forms

| | free trial package | p2p production license |
|---|---|---|
| How to seal | omit `ext04` | `ext04=customer node_pub` |
| Who can run it | Any MGC 1.5.4+ node | Only that customer node |
| Commercial meaning | Anyone can try it, wider reach | One license per customer, non-resellable |
| Customer changes machine | Runs as-is | Must be re-sealed |
| Renewal / upgrade | Ship a new version | Ship a new version |

> A free package cannot technically restrict who runs it; the trial boundary has to live in the script (for example, only return the first N periods, or add a watermark). To restrict per customer, use p2p.

## The production delivery chain

| Stage | Who | Action |
|---|---|---|
| 1. Assemble | Deliverer | Prepare a flat script folder, document dependencies and usage |
| 2. Fetch key | Customer | `mgc_get(info_type="__NODE_PUB__", info_owner="__NODE_PUB__")` and send it to the deliverer |
| 3. Dry run | Deliverer | Run locally on sample data; confirm no hardcoded paths |
| 4. Seal | Deliverer | `mgc_seal_package(..., ext04=customer_pub, output_dir=...)` |
| 5. Deliver | Deliverer | Send `.mgc_file`, dependency list, usage notes, and sha256 |
| 6. Import | Customer | `mgc_save_file(path="xxx.mgc_file", info_owner="...")` |
| 7. Run | Customer | `mgc_run(..., diff_3="run.py")`, results written locally |
| 8. Renew | Both | Re-seal for upgrades or machine changes; retire the old package |

## Four hard constraints

1. **Scripts go in, data does not.** Customer data stays on the customer side; sample CSVs are not shipped in the package. Non-script files inside a sealed package are plaintext.
2. **Flat directory.** Scripts saved into MGC must sit at the same `diff_2` level. No subdirectories; cross-script calls require the same `diff_2` (`DIFF2_MISMATCH`).
3. **Whole-folder seal, no file list.** p2p / free `mgc_seal_package` has **no `files` parameter** (`files` only exists inside chain-mode `ext04` array elements); the whole folder is sealed automatically, and `diff_3` is each file's relative path inside the package.
4. **Output must be written explicitly.** MGC does not create the parent directory of `--output`; the script must `mkdir(parents=True)` itself.

One compatibility note: **the builder needs MGC 1.6.0+, the customer's runner needs 1.5.4+, and cross-script calls need 1.5.2+**. If the customer node is older, import may succeed but cross-script calls will not route through sealed execution, and MGC returns a `TARGET_NODE_MAY_NOT_SUPPORT_AUTO_WORKFLOW` warning. Confirm the customer version before delivery.

## Runnable minimal example

`examples/` is a complete sales-forecast delivery package:

| File | Purpose |
|---|---|
| `prepare_sample_data.py` | Generates sample sales CSV (demo only, not shipped) |
| `model.py` | Forecast logic: moving average + growth rate, standard library only |
| `run.py` | Entry script, imports `model` at the same level, writes prediction JSON |
| `role_prompts.md` | Deliverer / customer briefs and licensing terms |

Local verification:

```bash
python examples/prepare_sample_data.py /tmp/delivery_demo/sales.csv
python examples/run.py --input /tmp/delivery_demo/sales.csv --output /tmp/delivery_demo/predictions.json
```

Sealed delivery:

```python
# Deliverer: store as a workflow package
mgc_save_file(path="./examples", info_owner="sales_forecast")

# Trial package: free mode, runnable on any MGC 1.5.4+ node
mgc_seal_package(
    info_owner="sales_forecast",
    diff_2="examples",
    output_dir="/tmp/delivery_demo/trial",
)

# Production package: p2p mode, bound to the customer node
mgc_seal_package(
    info_owner="sales_forecast",
    diff_2="examples",
    output_dir="/tmp/delivery_demo/licensed",
    ext04=customer_pub,
)
```

```python
# Customer: import and run
mgc_save_file(path="/tmp/delivery_demo/licensed/examples_delivery/examples.mgc_file",
              info_owner="sales_forecast")
mgc_run(info_type="script", info_owner="sales_forecast",
        diff_2="examples", diff_3="run.py")
```

> **Import note**: when importing a sealed package via `mgc_save_file`, the `info_owner` you pass applies to the **package group only**; every record inside keeps the owner recorded at seal time (the `INFO_OWNER_NOT_APPLIED` warning is advisory, not an error). After import, confirm with `mgc_find(info_owner="<the package's own owner>")` and use that value for all subsequent `mgc_run` calls — the 5+1 cross-script check requires caller and target to share the exact same `info_owner`, otherwise the call fails with `OWNER_MISMATCH`.

## Delivery checklist

Every delivery should include at least:

- The `.mgc_file` package
- `sha256`
- Dependency list (packages outside the standard library, with versions)
- Input format (columns, types, required fields)
- Output format (field meanings, units)
- Version number and change notes

## MGC tools quick reference

| Tool | Purpose |
|---|---|
| `mgc_get` | Fetch the customer node_pub (both `info_type` and `info_owner` must be `__NODE_PUB__`) / read licensing info |
| `mgc_save_file` | Store a workflow folder / import a `.mgc_file` |
| `mgc_seal_package` | Seal a workflow; omit `ext04` for a free trial package |
| `mgc_run` | Black-box execution, `diff_3` targets the entry script |
| `mgc_package` | Plaintext export within one trust domain (internal debugging) |
| `mgc_list` / `mgc_find` | Manage historical delivery versions |
| `mgc_delete` | Clean up expired packages |
| `mgc_skill` | Look up official parameters and artifact layout |

## Common failures

| Symptom | Cause | Fix |
|---|---|---|
| Import succeeds but `UNSEAL_FAILED` at run time | The package was forwarded to a non-licensed node, or `node_pub` is malformed | p2p packages are non-transferable; run on the licensed customer node and verify `node_pub` when re-sealing |
| `TARGET_NODE_MAY_NOT_SUPPORT_AUTO_WORKFLOW` | The customer's MGC is too old | Upgrade to ≥ 1.5.4 and re-import; cross-script calls need ≥ 1.5.2 |
| `DIFF2_MISMATCH` | `diff_2` is not the directory name | Confirm with `mgc_find` |
| Missing dependency on the customer side | An incomplete dependency list or a version mismatch | Ship `requirements.txt` with pinned versions |
| No output file produced | The `--output` parent directory does not exist | `mkdir(parents=True)` inside the script |

## Security boundary

- The deliverer gets: the customer's node_pub and the results the customer returns
- The deliverer does not get: the customer's raw data
- The customer gets: a runnable package and local output
- The customer does not get: source code or algorithm parameters

MGC protects content confidentiality; it does not provide online authentication or expiry. **Licensing has limits**: a p2p package is bound to a node, but it cannot stop a customer from observing inputs and outputs on that licensed machine. For stronger control, combine it with a contract and local audit logs. After unsealing, the script runs with the customer's permissions, and its reads, writes, and network behaviour are governed by the customer's environment.

## Contact

mirgincipher@outlook.com
