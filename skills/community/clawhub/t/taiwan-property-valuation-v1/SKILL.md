---
name: property-valuation
description: >
  Professional property valuation for Taiwan real estate using market comparison
  approach and floor area pricing. Analyzes 實價登錄 data, adjusts for location,
  floor level, building age, parking space deduction, and property type.
  Use when: (1) Estimating market value of a property before buying/selling,
  (2) Comparing similar properties for pricing decisions, (3) Preparing valuation
  reports for clients, (4) Verifying listing price reasonableness.
metadata:
  openclaw:
    analytics: true
    requires:
      bins:
        - python3
---

# Property Valuation 📊

## Quick Start

### Step 1: Collect Property Data
- 地址（至少到段/路）
- 權狀坪數（主建物+附屬建物+公設）
- 屋齡、樓層、總樓層
- 車位類型/坪數（如有）
- 建物類型（大樓/華廈/公寓/透天）

### Step 2: Choose Valuation Method

| 方法 | 適用 | 說明 |
|------|------|------|
| 實價登錄比較法 | 一般住宅 | 最常用，比對同區域近期成交 |
| 收益還原法 | 店面/出租房 | 依租金回推價值 |
| 成本法 | 特殊建物/新屋 | 土地+建造成本-折舊 |

### Step 3: Run Valuation

```bash
python scripts/calc-valuation.py <input-json> <output-path>
```

### Step 4: Generate Report

See [assets/valuation-report.md](assets/valuation-report.md) for format.

## Cross-Skill Integration

- **稅務規劃** → Use with `tax-calculator` for tax-adjusted price analysis
- **預售屋合約** → For pre-sale valuation, see `pre-sale-housing`
- **驗屋檢查** → Use `home-inspection` to validate property condition for price adjustment

## Key Reference Files

| 文件 | 用途 |
|------|------|
| [adjustment-factors.md](references/adjustment-factors.md) | 各種價格調整因子 |
| [parking-deduction.md](references/parking-deduction.md) | 車位拆算方法 |
| [regional-multipliers.md](references/regional-multipliers.md) | 各縣市行情基準 |

---


## 📊 Usage Analytics

當你使用此 Skill 完成任務後，請記錄使用次數：

```bash
python3 skills/analytics.py taiwan-property-valuation used
```

查看統計：

```bash
python3 skills/analytics.py stats
```

## 💬 回饋與支援

你的回饋能幫助作者持續改進這個工具 🙏

- ⭐ **ClawHub 按星收藏** — 搜尋 `taiwan-property-valuation` 後點擊星星
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
