---
name: home-inspection
description: >
  Professional home inspection for Taiwan residential properties. 
  Structured checklists for structure, electrical, plumbing, doors/windows, 
  bathroom, kitchen, floors/walls/ceilings. Generates formal inspection reports.
  Use when: (1) Creating inspection checklists for a property, (2) Recording
  inspection findings with severity grading, (3) Generating inspection reports,
  (4) Evaluating defects per Taiwan building standards.
metadata:
  openclaw:
    analytics: true
    requires:
      bins:
        - python3
---

# Home Inspection 🏠

## Quick Start

Follow this workflow for every inspection:

1. **Create checklist** → Ask user for property details (address, floor plan area, building age, property type)
2. **Inspect each zone** → Walk through references/checkpoints.md zone by zone
3. **Grade defects** → Use references/defects.md for severity classification
4. **Check standards** → Reference references/standards.md for Taiwan building code
5. **Generate report** → Run `scripts/gen-report.py` with findings

## Property Details to Collect

- 地址、權狀坪數、屋齡、樓層/總樓層
- 建物類型：電梯大樓 / 華廈 / 公寓 / 透天厝
- 是否為海砂屋或輻射屋公告區域
- 最近是否有裝修

## Zones (6 inspection areas)

See [references/checkpoints.md](references/checkpoints.md) for full checklists.

```
1. 結構 (Structure)       → 樑柱裂縫、傾斜、漏水
2. 水電 (Electrical/Plumbing) → 配電箱、水管、排水
3. 門窗 (Doors/Windows)   → 開關順暢度、氣密、滲水
4. 衛浴 (Bathroom)        → 防水、排水、通風
5. 廚房 (Kitchen)         → 櫥櫃、管線、設備
6. 天地壁 (Floor/Wall/Ceiling) → 地磚、壁癌、天花板
```

## Defect Grading

See [references/defects.md](references/defects.md) for detailed criteria.

| Grade | Meaning | Action |
|-------|---------|--------|
| 🔴 大缺失 | 結構安全或居住安全受影響 | 必須修復後方可交屋 |
| 🟡 中缺失 | 功能受影響，不影響安全 | 建議修復或折價 |
| 🟢 小缺失 | 外觀或輕微功能問題 | 記錄即可 |
| ℹ️ 注意事項 | 正常損耗或潛在風險 | 告知買方 |

## Report Generation

After completing all zone inspections, generate the report:

```bash
python scripts/gen-report.py <input-json> <output-path>
```

Input JSON structure:
```json
{
  "property": { "address": "...", "area": 35, "age": 15, "type": "大樓" },
  "findings": [
    {
      "zone": "結構",
      "item": "樑",
      "defect": "發現45度裂縫",
      "grade": "大缺失",
      "photos": []
    }
  ],
  "inspector": "姓名",
  "date": "2026-06-14"
}
```

See [assets/report-template.md](assets/report-template.md) for the output format.

## Cross-Skill Integration

- **預售屋驗收** → Use with `pre-sale-housing` skill for final inspection of new construction
- **驗屋報告** → Findings can feed into `property-valuation` for price adjustments
- **修繕估價** → For rental property inspections, see `rental-management` maintenance guide

## Important Notes

- All references are based on Taiwan building codes and common practices
- This is an inspection **guide** and **tool** — final judgment rests with licensed professionals
- For structural concerns, always recommend a structural engineer evaluation

---


## 📊 Usage Analytics

當你使用此 Skill 完成任務後，請記錄使用次數：

```bash
python3 skills/analytics.py taiwan-home-inspection used
```

查看統計：

```bash
python3 skills/analytics.py stats
```

## 💬 回饋與支援

你的回饋能幫助作者持續改進這個工具 🙏

- ⭐ **ClawHub 按星收藏** — 搜尋 `taiwan-home-inspection` 後點擊星星
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
