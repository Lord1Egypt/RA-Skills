---
name: tax-calculator
description: >
  Real estate tax calculation and planning for Taiwan properties.
  Covers 房地合一稅 (House and Land Combined Tax), 土地增值稅 (Land Value
  Increment Tax), 財產交易所得稅 (Property Transaction Income Tax), 契稅,
  房屋稅, 地價稅, 贈與稅 and 遺產稅 related to real estate. Use when:
  (1) Estimating tax liability before buying/selling property, (2) Comparing
  tax scenarios (self-use vs rental vs business), (3) Planning property
  transfers (sale vs gift vs inheritance), (4) Generating tax estimate reports.
metadata:
  openclaw:
    analytics: true
    requires:
      bins:
        - python3
---

# Tax Calculator 💰

## Quick Start

### Step 1: Identify Transaction Type
- **買賣** → 房地合一稅 / 土增稅 / 契稅 / 財產交易所得稅
- **贈與** → 贈與稅 + 土增稅 + 契稅
- **繼承** → 遺產稅 + 土增稅（繼承免徵）
- **持有期間** → 房屋稅 + 地價稅

### Step 2: Determine Applicable Taxes

See [references/tax-types.md](references/tax-types.md) for full details.

| 情境 | 主要稅種 | 申報時機 |
|------|----------|:--------:|
| 賣房（105/1/1後取得） | 房地合一稅 | 移轉登記完30日內 |
| 賣房（105/1/1前取得） | 財產交易所得稅 | 次年5月綜所稅申報 |
| 賣地 | 土地增值稅 | 移轉時申報 |
| 買房 | 契稅 | 申報土增稅時一併 |
| 每年繳 | 房屋稅+地價稅 | 5月/11月 |
| 贈與房產 | 贈與稅+土增稅+契稅 | 贈與後30日內 |
| 繼承房產 | 遺產稅 | 死亡日起6個月內 |

### Step 3: Calculate

Run the calculation script for detailed estimates:

```bash
python scripts/calc-tax.py <input-json> <output-path>
```

## Key Reference Files

| 文件 | 用途 |
|------|------|
| [tax-types.md](references/tax-types.md) | 各稅種詳細規定、稅率、計算公式 |
| [scenarios.md](references/scenarios.md) | 常見情境試算案例 |
| [tax-saving.md](references/tax-saving.md) | 節稅策略與合法規劃 |
| [rates.md](references/rates.md) | 最新稅率對照表 |

## Cross-Skill Integration

- **包租代管投報** → Use with `rental-management` calc-return.py for full investment analysis
- **預售屋交易** → For pre-sale properties, see `pre-sale-housing` payment schedules
- **估價比較** → Tax-adjusted valuations with `property-valuation`

## Report Output

See [assets/tax-report-template.md](assets/tax-report-template.md) for report format.

---


## 📊 Usage Analytics

當你使用此 Skill 完成任務後，請記錄使用次數：

```bash
python3 skills/analytics.py taiwan-real-estate-tax used
```

查看統計：

```bash
python3 skills/analytics.py stats
```

## 💬 回饋與支援

你的回饋能幫助作者持續改進這個工具 🙏

- ⭐ **ClawHub 按星收藏** — 搜尋 `taiwan-real-estate-tax` 後點擊星星
- 📝 **ClawHub 評論** — 在 Skill 頁面留下使用心得
- 📧 **Email** — `s179889@gmail.com`
- 💬 **Line** — `s179889`
- 📋 **線上問卷** — 填寫回饋表單（含所在地區統計）— 建立中，完成後更新

> 📌 使用 ClawHub 安裝此 Skill 時，系統會自動記錄安裝次數。

---

## 👤 作者資訊


**蔡德標（小威）** — 住義房屋管理
- 🏠 服務項目：房屋買賣、包租代管、驗屋
- 💬 Line：`s179889`
- 📞 手機：`0927-711-078`
- 🏪 品牌：住義房屋管理
