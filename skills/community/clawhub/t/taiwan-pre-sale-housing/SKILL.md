---
name: pre-sale-housing
description: >
  Comprehensive pre-sale housing (預售屋) purchase guide for Taiwan, covering
  the full lifecycle from red note negotiation (紅單), deposit, contract review,
  construction stage payments, interior modification requests, final inspection,
  to handover. Helps buyers navigate risks and legal protections specific to
  pre-sale properties. Use when: (1) Buying a pre-sale property, (2) Reviewing
  a pre-sale contract, (3) Managing construction stage payments, (4) Handling
  pre-sale disputes or delays.
metadata:
  openclaw:
    analytics: true
    requires:
      bins:
        - python3
---

# Pre-Sale Housing 🏗️

## Quick Start

### Pre-Sale Lifecycle

```
紅單 → 簽約 → 工程期款 → 對保 → 驗屋 → 交屋 → 管委會
```

### Stage 1: 紅單（購屋預約單）
| 要點 | 說明 |
|------|------|
| 本質 | 購屋意向書，非正式買賣契約 |
| 訂金 | 一般 10~30萬，可退（依建商規定）|
| 冷靜期 | 無法定冷靜期，但可主張民法撤銷 |
| 風險 | 建商可保留拒絕賣你的權利 |

### Stage 2: 簽約
See [references/contract-review.md](references/contract-review.md).

### Stage 3: 工程期款
See [references/payment-plan.md](references/payment-plan.md).

### Stage 4: 驗屋
See [references/final-inspection.md](references/final-inspection.md). Use with `home-inspection` skill.

### Stage 5: 交屋
See [references/handover.md](references/handover.md).

## Cross-Skill Integration

- **驗屋檢查** → Use `home-inspection` for final inspection checklist
- **稅務規劃** → Use `tax-calculator` for pre-sale tax planning
- **包租代管** → For pre-sale investment purposes, see `rental-management` return analysis

## Key Reference Files

| 文件 | 用途 |
|------|------|
| [contract-review.md](references/contract-review.md) | 預售屋合約審查要點 |
| [payment-plan.md](references/payment-plan.md) | 工程期款與對保流程 |
| [final-inspection.md](references/final-inspection.md) | 完工驗屋重點 |
| [handover.md](references/handover.md) | 交屋與管委會設立 |
| [disputes.md](references/disputes.md) | 常見預售屋糾紛與處理 |

---


## 📊 Usage Analytics

當你使用此 Skill 完成任務後，請記錄使用次數：

```bash
python3 skills/analytics.py taiwan-pre-sale-housing used
```

查看統計：

```bash
python3 skills/analytics.py stats
```

## 💬 回饋與支援

你的回饋能幫助作者持續改進這個工具 🙏

- ⭐ **ClawHub 按星收藏** — 搜尋 `taiwan-pre-sale-housing` 後點擊星星
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
