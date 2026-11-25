# Analytics and Algorithm Delivery

> **Version 1.0.0** · Requires MGC Blackbox ≥ 1.6.0

Free mode for the trial package, p2p mode for the production license. The customer runs locally, data never leaves their database, and the source stays unreadable.

## Use cases

- Independent analysts delivering forecasting / scoring / cleaning models
- Algorithm vendors deploying on-premise, licensed per customer node
- Internal tools productized: trial first, production later

## Install

```bash
pip install mgc-blackbox>=1.6.0
mgc
```

API `127.0.0.1:57219` / WebUI `127.0.0.1:57218`.

## Quick start

```bash
python examples/prepare_sample_data.py /tmp/delivery_demo/sales.csv
python examples/run.py --input /tmp/delivery_demo/sales.csv \
                       --output /tmp/delivery_demo/predictions.json
```

Sealed delivery:

```python
mgc_save_file(path="./examples", info_owner="sales_forecast")

# Trial package: no ext04
mgc_seal_package(info_owner="sales_forecast", diff_2="examples",
                 output_dir="/tmp/delivery_demo/trial")

# Production package: bound to the customer node
mgc_seal_package(info_owner="sales_forecast", diff_2="examples",
                 output_dir="/tmp/delivery_demo/licensed",
                 ext04=customer_pub)
```

## Layout

```
sealed-delivery-en/
├── SKILL.md
├── manifest.json
├── README.md
└── examples/
    ├── prepare_sample_data.py   # sample data (demo only)
    ├── model.py                 # forecast logic
    ├── run.py                   # entry script
    └── role_prompts.md          # briefs and licensing terms
```

## Two delivery forms

| | free trial package | p2p production package |
|---|---|---|
| Seal | omit `ext04` | `ext04=customer node_pub` |
| Who can run it | Any MGC 1.5.4+ node | Only that customer node |
| Best for | Wider reach | One license per customer |

> A free package cannot technically restrict who runs it; the trial boundary has to live in the script.

## Delivery checklist

`.mgc_file`, `sha256`, dependency list, input format, output format, version and change notes.

## Security boundary

MGC protects content confidentiality; it does not provide online authentication or expiry. A p2p package is bound to a node, but it cannot stop a customer from observing inputs and outputs on that licensed machine. After unsealing, the script runs with the customer's permissions. For stronger control, combine it with a contract and local audit logs.

## Contact

mirgincipher@outlook.com
