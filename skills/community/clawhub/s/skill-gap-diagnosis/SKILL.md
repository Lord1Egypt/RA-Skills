---
name: skill_gap_diagnosis
description: 業務缺口診斷 Skill。整合業績、競賽、榮譽、續保率、客戶增長、技能短板等多維數據，統一換算為保障保費口徑，計算缺口金額、需成交件數、緊急度/容易度標籤，按優先級排序，輸出多維度診斷結論。不輸出行動建議。在用戶表達「診斷」、「分析」、「整體情況」、「缺口」、「進度」、「還差多少」或同時詢問多個維度業績時觸發。禁止在單一指標查詢、單一排名查詢、閒聊、意圖不明時觸發。
metadata:
  openclaw:
    requires:
      env: ["API_BASE_URL"]
      tools:
        - Data_Performance
        - Data_Campaign
        - Data_Honor
        - Data_Renewal
        - Data_CustomerGrowth
        - Data_Skill
        - Data_Assessment
        - Data_NewAllowance
---

# 業務缺口診斷

## 核心职责

整合業績、競賽、榮譽、續保率、客戶增長、技能短板等多維數據，統一換算為保障保費口徑，計算缺口金額、需成交件數、緊急度/容易度標籤，按優先級排序，輸出多維度診斷結論。

**約束**：本 Skill 只輸出診斷結論，不輸出行動建議。行動建議由 skill_action_suggestion 統一生成。

## 觸發條件

### 正向觸發（滿足任一）

- 用戶明確表達「診斷」、「分析」、「整體情況」、「缺口」、「進度」、「還差多少」
- 用戶同時詢問多個維度業績（如競賽+榮譽+考核）
- 用戶說「我這個月業績怎麼樣」、「MDRT 進度如何」、「幫我看看缺口」

### 禁止觸發

- 用戶只問單一指標：「FYC 多少」、「保費多少」、「件數多少」 → 直接調對應 Tool
- 用戶只問單一排名：「競賽排名第幾」 → 直接調 Data_Campaign
- 閒聊/問候：「你好」、「在嗎」 → Agent 直接回復
- 意圖不明且未澄清：「幫我看看」 → Agent 反問澄清

## 執行流程

### 步驟 1：並行調用多維數據接口

並行調用以下接口，每個接口超時 10s，失敗時跳過該維度：

| 接口 | 參數 | 失敗策略 |
|:---|:---|:---|
| Data_Performance | dataType=ALL | 缺失業績基礎數據 |
| Data_Campaign | queryMode=FULL, hasGapOnly=true | 缺失競賽缺口 |
| Data_Honor | honorType=ALL | 缺失榮譽進度 |
| Data_Renewal | policyType=ALL | 缺失續保率 |
| Data_CustomerGrowth | 默認參數 | 缺失客戶增長 |
| Data_Skill | 默認參數 | 缺失技能短板 |
| Data_Assessment（可選） | assessmentType 按需 | 缺失考核數據 |
| Data_NewAllowance（可選） | 默認參數 | 缺失新人津貼 |

### 步驟 2：調用計算腳本

調用 `scripts/compute_gaps.py`，基於原始數據計算：

- 缺口金額 = target - actual
- 需成交件數 = ceil(缺口金額 / 件均保費)
- 緊急度標籤：截止 ≤7 天為「緊急」，≤30 天為「重要」，其餘為「常規」
- 容易度標籤：缺口 < 日均產能 × 剩餘天數時為「容易」
- 優先級排序：緊急度優先，其次按缺口金額降序

### 步驟 3：生成診斷文案

加載 `references/diagnosis.md`，將計算結果注入變量，生成診斷文案。

**約束**：
- 禁止機械編號（如「1. 2. 3.」列表）
- 禁止暴露接口名稱（不出現 Data_Performance 等）
- 金額保留原始單位（HKD）
- 排名數據必須附加時效提示：「數據截至 {dataAsOfDate}，由於排名會隨時間動態變化，請以實際達標情況為準」
- 禁止承諾結果
- daysRemaining > 60 不提及倒數天數

## 輸入參數

見 schema/input.json

## 輸出格式

見 schema/output.json

## 異常與降級

| 異常場景 | 處理策略 | 用戶感知 |
|:---|:---|:---|
| 單個 API 超時 | 跳過該維度，缺失字段返回 null | 「XX數據暫時無法獲取，以下為基於其他維度的分析」 |
| 全部 API 不可用 | 降級知識庫模式 | 「當前無法獲取實時數據，以下為通用建議」 |
| 件均保費缺失 | requiredCases 返回 null | 跳過件數建議，聚焦金額缺口 |
| 無缺口數據 | gapIndicators 返回空數組 | 「恭喜，您當前無未達標缺口」 |
| 考核資格不符 | 該考核不納入 gapIndicators | 不展示無資格考核 |

## 業務規則

- 緊急度：截止 ≤7 天為「緊急」，≤30 天為「重要」，其餘為「常規」
- 容易度：缺口 < 日均產能 × 剩餘天數時為「容易」
- 金額精度：保留兩位小數，單位 HKD
- 排名數據必須提示時效性
- daysRemaining > 60 不提及倒數天數
