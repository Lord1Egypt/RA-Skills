---
name: aws-price-csv
description: Generate AWS cost CSVs from a user-provided service list. Use when someone supplies an item list + AWS region and needs per-item pricing plus totals via AWS Price List API or bulk pricing JSON.
---

# AWS Price CSV Skill

## Overview
Transforms a user-provided AWS service list (instances, volumes, S3 buckets, etc.) into a pricing CSV. The script can query the AWS Price List API (via `aws-cli`) or reuse cached bulk JSON files. It supports On-Demand and Reserved terms and automatically adds up per-item and total costs.

## Quick Start
1. Prepare a YAML/JSON file with `name`, `service_code`, `filters`, `term`, and `usage` fields (see sample in `references/api_reference.md`).
2. Pick the data source:
   - **API mode** – requires `aws pricing get-products` permission and an internet connection.
   - **Bulk mode** – no IAM access required; the script downloads/caches public bulk JSON files.
3. Run the script with the region and desired options:
   ```bash
   python3 scripts/generate_pricing_csv.py \
     --input inputs/sample.yml \
     --region ap-northeast-1 \
     --source bulk \
     --cache-dir ~/.cache/aws-price-csv \
     --output quotes/apac_quote.csv
   ```
4. Inspect the CSV (each line item + TOTAL) and deliver alongside the original request if needed.

## Workflow

### 1. Prepare the input list
- Use the YAML/JSON templates in `references/api_reference.md`.
- `filters` must map to AWS pricing attributes (`instanceType`, `regionCode`, `volumeApiName`, `usagetype`, `termType`, etc.).
- `term.type`: `OnDemand` or `Reserved` (`RI`).
- `term.attributes` (optional) filter Reserved prices (`LeaseContractLength`, `PurchaseOption`, `OfferingClass`, ...).
- `usage.quantity` represents the amount to multiply (hours, GB-Mo, requests, ...).

### 2. Choose the data source
| Mode | When to use | Notes |
|------|-------------|-------|
| API (`--source api`) | You already have IAM creds and want real-time data | Uses `aws pricing get-products` in `us-east-1` |
| Bulk (`--source bulk`) | Offline, no IAM, or you want caching | The script checks `--cache-dir` (default `~/.cache/aws-price-csv`); cached files newer than 30 days are reused, otherwise they are re-downloaded |

> You can still override with `--bulk-files ServiceCode=/path/to/file.json`; those files win over the cache.

### 3. Generate the CSV
- Script path: `scripts/generate_pricing_csv.py`
- Key arguments:
  - `--input`: YAML/JSON list
  - `--region`: AWS region code (location name is auto-added to filters)
  - `--output`: CSV path (default `aws_pricing.csv`)
  - `--source`: `api` (default) or `bulk`
  - `--cache-dir`: bulk cache directory (default `~/.cache/aws-price-csv`)
  - `--force-refresh`: ignore cached bulk files and re-download
  - `--bulk-files`: `ServiceCode=/path/to/file.json` overrides the cache
- Output columns: `item_name, service_code, term_type, region, location, quantity, usage_unit, price_unit, price_per_unit_usd, cost_usd, description`, plus a `TOTAL` row.

### 4. Validate & deliver
- Review the CSV to ensure every line item has pricing and a description.
- Confirm the `TOTAL` matches expectations.
- Include the source list or any supporting docs if required.

## Troubleshooting
| Issue | Fix |
|-------|-----|
| `aws pricing` returns empty results | Double-check filters (location, regionCode, termType, etc.) or fall back to bulk mode |
| `aws` CLI missing | Install aws-cli v2, configure credentials, or rely on bulk mode |
| Need to refresh cached data | Use `--force-refresh` or delete the cached JSON so it gets re-downloaded |
| PyYAML missing | `pip install pyyaml` or convert input to JSON |
| Reserved price not found | Add `LeaseContractLength`, `PurchaseOption`, `OfferingClass` inside `term.attributes` |

## Resources
- `scripts/generate_pricing_csv.py` – main script with API/bulk support, caching logic, and On-Demand/Reserved handling.
- `references/api_reference.md` – Price List API examples, bulk download pointers, region/location table, and sample input templates (including gp3 and RI cases).
