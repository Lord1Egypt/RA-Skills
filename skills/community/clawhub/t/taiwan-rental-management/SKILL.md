---
name: rental-management
description: >
  End-to-end property rental management SOP for Taiwan, covering the full
  landlord lifecycle: tenant sourcing, screening, lease signing, move-in/move-out
  inspection, maintenance handling, rent collection, dispute resolution, and
  lease renewal/termination. Supports both self-managed and 包租代管 (agency-managed)
  models. Use when: (1) Managing a rental property, (2) Training new property
  managers, (3) Setting up rental management systems, (4) Handling landlord-tenant
  disputes, (5) Planning property maintenance schedules.
metadata:
  openclaw:
    analytics: true
    requires:
      bins:
        - python3
---

# Rental Management 🏢

## Quick Start

### Identify Management Model

| 模式 | 說明 | 適合對象 |
|------|------|----------|
| 自租自管 | 房東自己管理 | 1-5間物件 |
| 代管模式 | 房東收租，業者管雜務 | 繁忙房東 |
| 包租模式 | 業者包租再轉租 | 不想煩惱的房東 |
| 委託管理 | 房仲/物管代管 | 5-20間以上 |

### Full Lifecycle

1. **前置準備** → 法規、稅務、保險
2. **招租** → 定價、曝光、帶看
3. **篩選房客** → 身分確認、收入證明、聯徵
4. **簽約** → 使用 team-lease-review 或內建模板
5. **點交** → 設備清單、拍照存檔
6. **管理期間** → 收租、修繕、回報
7. **續約／解約** → 續約條件、點交返還
8. **糾紛處理** → 調解、存證信函、訴訟

## Key Reference Files

| 文件 | 用途 |
|------|------|
| [lifecycle.md](references/lifecycle.md) | 完整8階段操作流程 |
| [tenant-screening.md](references/tenant-screening.md) | 房客審核SOP |
| [maintenance.md](references/maintenance.md) | 修繕分類與處理 |
| [disputes.md](references/disputes.md) | 常見糾紛與處理方式 |
| [agency.md](references/agency.md) | 包租代管合約要點 |

## Cross-Skill Integration

- **租約審查** → Use with `lease-review` for contract analysis before signing
- **稅務規劃** → Use with `tax-calculator` for rental income tax estimation
- **驗屋檢查** → For move-in/move-out inspections, use `home-inspection`

## Useful Scripts

```bash
# 租金報酬率試算
python scripts/calc-return.py <input-json> <output-path>
```

---


## 📊 Usage Analytics

當你使用此 Skill 完成任務後，請記錄使用次數：

```bash
python3 skills/analytics.py taiwan-rental-management used
```

查看統計：

```bash
python3 skills/analytics.py stats
```

## 💬 回饋與支援

你的回饋能幫助作者持續改進這個工具 🙏

- ⭐ **ClawHub 按星收藏** — 搜尋 `taiwan-rental-management` 後點擊星星
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
