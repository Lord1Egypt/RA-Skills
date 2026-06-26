---
name: tw-monthly-revenue
description: 台股月營收抓取與分析。從公開資訊觀測站(MOPS)取得上市/上櫃公司當月營收，計算YoY/MoM年增率與月增率，輸出BEAT/MISS/NEUTRAL信號。用於：(1)月營收公布後自動分析 (2)觸發投資Pipeline決策 (3)更新ANALYSIS_INDEX監控條件
---

# 台股月營收分析

## 使用方式

```bash
# 自動抓上個月（每月10日後執行）
python3 ~/.openclaw/workspace/skills/tw-monthly-revenue/scripts/tw_monthly_revenue.py

# 指定月份
python3 ~/.openclaw/workspace/skills/tw-monthly-revenue/scripts/tw_monthly_revenue.py 2026-03
```

## 資料來源

公開資訊觀測站 (MOPS)：https://mops.twse.com.tw
- 上市公司 (sii)：台塑、南亞、台化、旺宏、材料-KY
- 台股月營收每月 10 日前公布（上月數字）

## BEAT/MISS 定義

| 信號 | 年增率條件 |
|------|-----------|
| BEAT | YoY ≥ +10% |
| NEUTRAL | -10% < YoY < +10% |
| MISS | YoY ≤ -10% |

## 追蹤標的

修改腳本中的 `WATCHLIST` 字典來新增/移除標的。
目前追蹤：2337（旺宏）、4763（材料-KY）、1301（台塑）、1303（南亞）、1326（台化）

## 輸出格式

```json
{
  "period": "2026-03",
  "stocks": {
    "2337": {
      "name": "旺宏",
      "revenue_m": 1234567,
      "yoy_pct": 26.0,
      "mom_pct": 12.2,
      "cumulative_yoy": 18.5,
      "signal": "BEAT"
    }
  }
}
```
