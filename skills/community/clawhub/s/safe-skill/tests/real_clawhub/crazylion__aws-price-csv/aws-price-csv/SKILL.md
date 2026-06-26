---
name: aws-price-csv
description: Generate AWS cost CSVs from a user-provided service list. Use when someone supplies an item list + AWS region and needs per-item pricing plus totals via AWS Price List API or bulk pricing JSON.
---

# AWS Price CSV Skill

## Overview
將使用者提供的 AWS 服務清單與區域轉換成定價 CSV，內容包含各項次的單價、用量、成本總計。預設透過 AWS Price List API（aws-cli），亦可在離線狀況使用 bulk pricing JSON，並支援 On-Demand 與 Reserved（RI）條件。

## Quick Start
1. 取得輸入檔（YAML/JSON），欄位至少包含 `name`, `service_code`, `filters`, `term`, `usage.quantity`, `usage.unit`。
2. 確認 aws-cli 已設定 `pricing:GetProducts` 權限（僅支援 `us-east-1`）。
3. 執行腳本並指定區域：
   ```bash
   python3 scripts/generate_pricing_csv.py \
     --input inputs/sample.yml \
     --region ap-northeast-1 \
     --output quotes/apac_quote.csv
   ```
4. 檢查輸出 CSV（每筆項目 + TOTAL 列），若需要可附上原始清單一併交付。

## Workflow

### 1. 準備輸入清單
- 使用 `references/api_reference.md` 內的範例格式（支援 YAML / JSON）。
- `filters` 的欄位需對應 AWS 定價屬性（`instanceType`, `termType`, `usagetype`, `volumeType`…）。
- `term.type`：`OnDemand` 或 `Reserved`（可用 `RI`）。
- `term.attributes`（選填）：對 Reserved 定價指定 `LeaseContractLength`, `PurchaseOption`, `OfferingClass` 等條件。
- `usage.quantity` 代表計費單位的用量（小時、GB-Mo、Requests...）。

### 2. 選擇資料來源
| 模式 | 適用情境 | 設定方式 |
|------|-----------|-----------|
| API (`--source api`) | 一般情境，需連線與 AWS IAM | 需要 aws-cli 可用且有 `pricing:GetProducts` 權限 |
| Bulk (`--source bulk`) | 離線或無 IAM 的環境 | 先從 AWS 公開 S3 下載 bulk JSON。啟動腳本時以 `--bulk-files ServiceCode=/path/to/json` 指定 |

範例：
```bash
python3 scripts/generate_pricing_csv.py \
  --input inputs/rds.yml \
  --region ap-northeast-1 \
  --source bulk \
  --bulk-files AmazonRDS=cache/AmazonRDS_ap-northeast-1.json
```

### 3. 產出 CSV
- 腳本路徑：`scripts/generate_pricing_csv.py`
- 主要參數：
  - `--input`: YAML/JSON 清單路徑
  - `--region`: AWS Region Code（會自動轉成 location 名稱加入過濾條件）
  - `--output`: CSV 檔名（預設 `aws_pricing.csv`）
  - `--source`: `api`（預設）或 `bulk`
  - `--bulk-files`: `ServiceCode=/path/to/json`（bulk 模式必填，可多次）
- 輸出欄位：`item_name, service_code, term_type, region, location, quantity, usage_unit, price_unit, price_per_unit_usd, cost_usd, description` + `TOTAL` 列。

### 4. 驗證與交付
- 讀取 CSV，確定每個項次都有價格與說明。
- 確認 `TOTAL` 總額是否符合使用者期望。
- 需要附上來源清單或中繼資料時，可將輸入與輸出一起壓縮。

## Troubleshooting
| 問題 | 處理方式 |
|------|-----------|
| `aws pricing` 回傳空集合 | 檢查 `filters` 是否缺少 `termType/location/regionCode`，或換用 bulk JSON |
| `aws` 命令不存在 | 安裝 aws-cli v2 並設定憑證，或改用 bulk 模式 |
| PyYAML 缺失 | `pip install pyyaml` 或將輸入改為 JSON |
| Bulk JSON 過大 | 先在本地快取（`curl -o AmazonEC2_ap-northeast-1.json https://pricing...`），再透過 `--bulk-files` 指定 |
| Reserved 找不到對應 | 在 `term.attributes` 補上 `LeaseContractLength`, `PurchaseOption`, `OfferingClass` |

## Resources
- `scripts/generate_pricing_csv.py`：主腳本，支援 API / bulk 以及 On-Demand / Reserved。
- `references/api_reference.md`：Price List API 命令範例、bulk JSON 下載連結、區域與 location 對照，以及輸入樣板（含 RI）。
