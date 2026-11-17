# 法学实证卡（empirical-legal）

> 招式定位：描述 / 比较 / 因果 / 批判评价。学科轴：法学实证（新增轴）。
> 与 `cards/econometrics.md`（DID/IV/RDD）、`cards/data-analysis.md` 互补：法律实证是它们的"法律场景化"。

## 适用场景
- 法律改革/判例的**实际效果**（不只是规范分析"应当如何"）。
- 司法行为（法官、陪审团、检察官决策）、法律执行、歧视/公平等可量化法律问题。
- 法教义学之外，要"法律在真实世界怎么运作"。

## 常用方法
- **法律语料/案例统计**：案例库（如 CourtListener、北大法宝）做描述统计、趋势、网络分析（引用网络）。
- **田野实验 / 审计研究（audit study）**：随机分配情境（如简历种族/性别）测歧视——劳动/住房/司法公平经典法。
- **自然实验**：法院裁定/法律变更作为外生冲击 → DID / RDD / 断点（见 `cards/econometrics.md`）。
- **司法决策建模**：判决预测、量刑差异 → `cards/ml-eval.md`（但谨慎：公平/可解释优先）。
- **调查/问卷**：公众法律意识、守法行为 → `cards/survey-scale.md`。

## 前提
- 法律数据常"非随机可得"——公开判决有选择性，需识别可得性偏倚。
- 因果识别需外生变异（改革时点/随机分配），否则只是相关。

## 常见坑
- **规范/实证混淆**：把"法应如此"当"法实如此"——实证要测实际，不替价值立场。
- **选择偏倚**：只分析上诉/公开案例，忽略未上诉的大多数（幸存者偏差）。
- **DID 前提未验**：平行趋势假设不画、不验，因果 claim 虚。
- **公平误用**：ML 判决预测若用敏感属性或代理变量，易放大量化歧视——见 `cards/ml-eval.md` 公平节。

## 何时换招
- 纯法律解释/教义 → `cards/humanities.md`（法律诠释属人文轴）。
- 要因果识别技术 → `cards/econometrics.md`。
- 要描述统计 → `cards/data-analysis.md`。

## 经典出处
- *The Oxford Handbook of Empirical Legal Research*（书单 #7，Cane & Kritzer 编 2010）——领域总览。
- 方法技术见 `cards/econometrics.md`（DID/RDD/IV）与 `cards/experiment-design.md`（田野实验）。
