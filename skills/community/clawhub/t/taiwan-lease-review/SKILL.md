---
name: lease-review
description: >
  Professional lease contract review for Taiwan rental agreements. 
  Supports residential, commercial/storefront, and parking space leases.
  Analyzes clauses for illegality, unfairness, and risk per Taiwan's
  Lease Protection Act (租賃專法) and standardized contract rules.
  Use when: (1) Reviewing a rental agreement before signing, (2) Checking
  if specific clauses are legal/enforceable, (3) Comparing tenant vs landlord
  rights, (4) Rewriting risky clauses to fair versions.
metadata:
  openclaw:
    analytics: true
    requires:
      bins:
        - python3
---

# Lease Review 📄

## Quick Start

1. **Identify lease type** → 住宅租約 / 店面商用租約 / 車位租約
2. **Scan for illegal clauses** → Compare against references/illegal-clauses.md
3. **Check mandatory items** → Ensure all required items are present via references/mandatory-items.md
4. **Grade each clause** → Use references/risk-levels.md for risk classification
5. **Reference specific law** → See references/rental-law.md for legal basis
6. **Check special types** → 
   - 店面/商用：references/commercial-lease.md
   - 車位：references/parking-lease.md
7. **Generate report** → Run `scripts/analyze-contract.py` if structured input

## Lease Type Quick Reference

### 住宅租約
- 適用：租賃專法（住宅租賃定型化契約應記載及不得記載事項）
- 特色：保護承租人較多，押金上限2個月

### 店面/商用租約
- 適用：普通民法租賃（不完全適用租賃專法）
- 特色：較多議約空間，注意營業登記、裝修條款

### 車位租約
- 適用：民法租賃（通常另有管委會停車管理辦法）
- 特色：注意是否為法定停車位/增設停車位

## Risk Levels

See [references/risk-levels.md](references/risk-levels.md) for full criteria.

| Level | Meaning |
|-------|---------|
| 🔴 違法條款 | 違反強制規定，條款無效 |
| 🟡 高風險 | 對一方極不利，建議修改 |
| 🟢 低風險 | 可接受，但需留意 |
| ✅ 標準條款 | 符合法規，建議保留 |

## Key Legal References

| Topic | File |
|-------|------|
| 不得記載事項 | [illegal-clauses.md](references/illegal-clauses.md) |
| 應記載事項 | [mandatory-items.md](references/mandatory-items.md) |
| 租賃專法重點 | [rental-law.md](references/rental-law.md) |
| 風險分級機制 | [risk-levels.md](references/risk-levels.md) |
| 店面商用特別事項 | [commercial-lease.md](references/commercial-lease.md) |
| 車位特別事項 | [parking-lease.md](references/parking-lease.md) |

## Cross-Skill Integration

- **包租代管** → Use with `rental-management` skill for the full landlord lifecycle
- **商用店面** → For property valuation of storefronts, see `property-valuation`
- **合約模板** → Rental agreement templates available in `rental-management` lifecycle

## Report Generation

For structured analysis, use the analysis script:

```bash
python scripts/analyze-contract.py <input-json> <output-path>
```

See [assets/review-report.md](assets/review-report.md) for the output format.

---


## 📊 Usage Analytics

當你使用此 Skill 完成任務後，請記錄使用次數：

```bash
python3 skills/analytics.py taiwan-lease-review used
```

查看統計：

```bash
python3 skills/analytics.py stats
```

## 💬 回饋與支援

你的回饋能幫助作者持續改進這個工具 🙏

- ⭐ **ClawHub 按星收藏** — 搜尋 `taiwan-lease-review` 後點擊星星
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
