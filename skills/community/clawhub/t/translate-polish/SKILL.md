---
name: translate-polish
description: |
  AI 中英互译与译文润色工作流。覆盖译前准备（领域/受众/语气/术语表）、分块翻译、两遍校对（准确性+流畅度）、术语一致性校验、文化适配；内置术语一致性校验脚本。适用于论文、商务信函、技术文档、营销文案的翻译与精修。
version: 1.0.0
author: WorkBuddy
agent_created: true
visibility: "public"
tags:
  - translation
  - 翻译
  - 润色
  - polish
  - 术语一致性
---

# translate-polish — AI 翻译润色工作台

_把"一次性机翻"升级为"专业译后精修"的可复用流程。质量不靠模型运气，靠流程。_

## 核心理念（来自 2025 一线实践）

1. **译前准备 > 译后修补**：源文质量决定译文上限。翻译前先澄清领域、受众、语气、地区（US/UK、简中/繁中）。
2. **术语护城河**：建术语表（glossary）+ 禁译表（DNT），强制一致性。专业名词错译率可从 15% 降到 3%。
3. **语境优先于碎片**：整段/整句翻译并附上下文，不要逐句丢给模型。
4. **两遍校对**：Pass1 校准确性（术语/事实/数字/人名/链接），Pass2 校流畅度（可读性/语气/衔接）。
5. **共识翻译**：关键内容用多模型交叉验证，少数派错误会被多数票掉。
6. **持续进化**：收集译后修正记录，沉淀术语库与 Translation Memory。

## 标准工作流

### 1. 译前 brief（一句话随文携带）
```
[领域] 计算机科学 / 法律合同 / 医疗器械 / 营销
[受众] 期刊审稿人 / 终端消费者 / 监管者
[语气] 正式学术 / 商务正式 / 友好口语
[地区] 美式 / 英式 / 简中 / 繁中
[禁译] 品牌名、产品SKU、代码变量保持原文
```

### 2. 源文预处理
- 拆长句为短陈述句（多从句的长句更易译错）
- 首字母展开缩写（MT → machine translation）
- 消解指代歧义（this/it/they 补出真实名词）
- 统一术语（同一概念不要 client/customer/end user 混用）

### 3. 分块翻译（长文）
按 500–800 字/块切分，附术语表与领域关键词（论文摘要+关键词先给模型建立领域认知）。
可调用 `long-text-summarizer` 的分块器 `chunker.py` 先切，再逐块喂译。

### 4. 术语一致性校验（脚本）
翻译完成后，用本技能脚本校验约定术语是否被遵守：
```bash
python scripts/glossary_check.py <译文文件> --glossary glossary.json
```
`glossary.json` 格式：
```json
{
  "人工智能": "Artificial Intelligence",
  "神经网络": "Neural Network",
  "wafer": "晶圆"
}
```
脚本报告：哪些源术语出现但目标术语缺失/不一致。

### 5. 两遍校对
- **Pass1 准确性**：逐条核对术语、事实、数字、人名、链接、占位符 `{x}`/`%s`、HTML/Markdown 标签是否被破坏。
- **Pass2 流畅度**：读 aloud 或 TTS 抓拗口处；强化学术风格（"We think"→"The findings suggest"）、量化表述（"good results"→"a 15.2% improvement"）。

### 6. 文化适配
- 识别文化特定表达（"摸着石头过河"→"trial-and-error approach"）
- 隐喻本地化（"黑箱模型"→"opaque model" 而非直译 "black box model"）
- 地区变体（soccer/football, color/colour）

## 自我进化学习系统

本技能使用 `scripts/learner.py` 记录每次翻译任务的成败与高频错误模式：

```bash
# 记录一次翻译（成功）
python scripts/learner.py record <技能目录> --capability 术语一致性 --note "用户要求法律合同连带责任译法"

# 记录一次失败（错误类型会被累计）
python scripts/learner.py record <技能目录> --capability 文化适配 --fail --error 文化误译 --note "成语直译导致歧义"

# 查看累计洞察
python scripts/learner.py insight <技能目录>

# 自动复盘：某错误累计≥3次→建议加预检；操作≥10次→高低频分析
python scripts/learner.py reflect <技能目录>
```

记忆落盘在 `learned_patterns.json`，跨会话持续积累，使本技能越用越准。

## 安全边界
- 敏感/涉密文本切勿外发到第三方翻译 API；优先本地模型或脱敏后处理。
- 法律/医疗关键文件保留 100% 人工复审，AI 仅做预翻译+精修建议。
- 不翻译密级文档、个人隐私数据。
