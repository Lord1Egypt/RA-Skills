---

name: spin-sales
description: 终极版 SPIN 销售法专家系统 - 提供从开场、挖掘、到促成的全周期、可操作的销售对话脚本框架。适用于复杂的 B2B 销售咨询场景。
author: mikewongonline
metadata: {"openclaw":{"emoji":"🎯","requires":["memory_search","tavily_search"]}}
---

---

# 🎯 SPIN-SALES - 终极版 SPIN 销售法专家系统（V3.5）

## 🎯 技能目标

提供完整的 SPIN 销售法框架，从开场到促成，模拟专业销售咨询过程，最终生成可执行的项目计划。

**使用边界**: 仅适用于复杂 B2B 销售咨询，不处理简单功能演示或价格询价。

---

## 📚 **核心框架：SPIN 四问法**

| 字母 | 中文名称 | 英文全称 | 目的 | 典型问题示例 |
|------|---------|---------|------|-------------|
| **S** | 背景问题 | Situation Questions | 了解客户现状、流程和基本信息 | "您目前是如何管理客户数据的？" "现有的 CRM 系统是什么品牌？" |
| **P** | 难题问题 | Problem Questions | 探明客户的痛点、困难和不满 | "数据延迟的频率如何？" "有哪些功能让客户投诉最多？" |
| **I** | 影响问题 | Implication Questions | 放大问题后果，创造紧迫感 | "这个问题导致客户流失了吗？" "如果持续存在有什么影响？" |
| **N** | 需求效益 | Need-Payoff Questions | 让客户说出解决方案的价值 | "如果能实时追踪，对团队意味着什么？" "能带来哪些改进？" |

---

## 🎯 **销售流程四阶段**

### **Stage 1: Opening（开场）**
- **目标**：建立信任，了解客户现状
- **方法**：提出 Situation 背景问题
- **话术模板**："今天想了解贵公司的 XX 情况，能先问几个基本情况吗？"

### **Stage 2: Investigating（调查）**
- **目标**：深入挖掘痛点和挑战
- **方法**：Problem + Implication 问题组合
- **关键点**：多问开放式问题，让客户多说（80% 时间给客户）

### **Stage 3: Demonstrating Capability（展示能力）**
- **目标**：呈现解决方案如何匹配客户需求
- **方法**：Need-Payoff 问题引导价值主张
- **技巧**：让客户自己说"这正是我需要的"

### **Stage 4: Obtaining Commitment（获得承诺）**
- **目标**：引导客户做出购买决策
- **方法**：处理异议，明确下一步行动
- **重点**：让客户主动承诺，而非被动接受

---

## 📊 **Neil Rackham 研究发现**

基于**35,000+ 次销售电话录音分析**的关键结论：

- ✅ **复杂型交易**（高价值、多决策者）更适合 SPIN
- ✅ **简单型交易**可使用简化版 S.P. + N 框架
- ✅ **Top performers ask 4x more Implication questions** than average
- ✅ **问题比例控制**：Situation: 10-15%, Problem: 25-30%, Implication: 30-40%, Need-Payoff: 25-30%

---

## 🎯 **核心原则与最佳实践**

### **5 项黄金法则：**

1. **顺序不可跳跃** - Situation → Problem → Implication → Need-Payoff
2. **问题比例控制** - Implication 问题要占最高优先级（30-40%）
3. **开放式问题优先** - "如何"比"是什么"更好，避免 Yes/No 封闭式问题
4. **聆听大于讲述** - 80% 时间让客户说，20% 销售说
5. **让客户自己说出口** - "你们需要这个功能" → "这对您的团队意味着什么？"

### **⚠️ 常见错误对比：**

> ❌ **特征推销**: "我们有 X、Y、Z 功能，能帮您..."
> → 客户回应："我们不关心那些功能，我们只需要解决 A 问题。"
>
> ✅ **SPIN 提问**: "您在解决 A 问题时遇到什么挑战？理想方案对团队有何价值？"
> → 客户回应："这正是我们需要解决的痛点！"

---

## 🔄 **适用场景与限制**

### ✅ **最佳适用场景：**
- **复杂型销售**（高价值、长周期、多决策者）
- **B2B 企业级销售**
- **解决方案型产品销售**
- **咨询服务/软件 SaaS**
- **客户关系型业务**

### ⚠️ **限制与不适用：**
- **简单交易**（低单价、单次购买、冲动消费）
- **冲动型消费者**（需要快速决策的场景）
- **竞争对手激烈、价格敏感的市场**
- **个人消费品零售场景**

---

## 🛠️ **脚本接口参考**

本技能将核心实现封装在 `scripts/` 目录中，SKILL.md 仅描述接口签名和使用方式。完整的代码实现请直接查看对应脚本文件。

### 1️⃣ SPIN 问题序列生成器 → `scripts/question_generator.py`

```python
generate_spin_questions(industry: str, product: str) -> dict
```

- **功　能**: 根据行业和产品自动生成 S/P/I/N 四阶段提问列表
- **返回值**: `{industry, product, questions_by_stage: {situation:[], problem:[], implication:[], need_payoff:[]}}`
- **使用示例**:
  ```python
  questions = generate_spin_questions("物流", "车队管理系统")
  questions["questions_by_stage"]["situation"]  # → 5 个背景问题
  ```
- **完整源码**: [scripts/question_generator.py](scripts/question_generator.py)

---

### 2️⃣ SPIN 流程演示 → `scripts/basic_demo.py`

```python
run_spin_demo()
```

- **功　能**: 使用 `question_generator` + `state machine` 展示一次完整的 S-P-I-N 销售流程
- **使用方式**: `python scripts/basic_demo.py`
- **完整源码**: [scripts/basic_demo.py](scripts/basic_demo.py)

---

### 3️⃣ 开场白生成器 → `scripts/opening.py`

```python
get_industry_context(industry: str) -> dict
generate_insightful_opener(industry: str) -> str
execute_opening_ritual(industry: str = None)
```

- **功　能**: 根据行业（金融科技/医疗/制造/物流等）生成具备洞察力的开场白话术
- **使用方式**: `python scripts/opening.py --industry 医疗`（支持 4 种预设行业）
- **完整源码**: [scripts/opening.py](scripts/opening.py)

---

### 4️⃣ SPIN 流程状态机 → `scripts/demo_interview.py`

```python
class SpinStateMachine:
    get_situation_question(industry) -> List[str]
    get_problem_question(industry)    -> List[str]
    get_implication_question(industry) -> List[str]
    get_need_payoff_question(industry) -> List[str]
    check_and_redirect(client_speaking_time: float) -> bool
    generate_action_plan() -> dict
```

- **功　能**: 控制 S-P-I-N 四阶段状态流转，监控 80/20 法则，生成 SMART 行动计划

---

### 3️⃣ SPIN 流程状态机 → `scripts/demo_interview.py`

```python
class SpinStateMachine:
    get_situation_question(industry) -> List[str]
    get_problem_question(industry)    -> List[str]
    get_implication_question(industry) -> List[str]
    get_need_payoff_question(industry) -> List[str]
    check_and_redirect(client_speaking_time: float) -> bool
    generate_action_plan() -> dict
```

- **功　能**: 控制 S-P-I-N 四阶段状态流转，监控 80/20 法则，生成 SMART 行动计划
- **使用方式**: `python scripts/demo_interview.py`
- **完整源码**: [scripts/demo_interview.py](scripts/demo_interview.py)

---

## 📖 **问题模板库**

`references/` 目录包含 SPIN 四阶段深度提问模板及异议处理指南，按阶段分文件管理：

| 文件 | 阶段 | 内容概要 | 文件大小 |
|------|------|---------|---------|
| [s-questions.md](references/s-questions.md) | **S** 背景问题 | 现状调研、流程诊断、基本信息采集 | 5.3 KB |
| [p-questions.md](references/p-questions.md) | **P** 难题问题 | 痛点挖掘、成本问题、满意度探询 | 4.0 KB |
| [i-questions.md](references/i-questions.md) | **I** 影响问题 | 时间/财务/战略/人员影响放大 | 4.6 KB |
| [n-questions.md](references/n-questions.md) | **N** 需求效益 | 价值引导、效益量化、行动承诺 | 16.6 KB |
| [objections.md](references/objections.md) | 异议处理 | 常见客户异议应对策略及话术 | 12.8 KB |
| [opening_scripts.md](references/opening_scripts.md) | 开场话术 | 各行业开场白脚本模板大全 | 11.8 KB |

---

## 📝 **实战对话示例**

### **场景：企业级客户关系管理（CRM）系统销售**

> **销售顾问**: "王总您好，今天想了解贵公司目前的供应链管理情况。不介意的话，我先问几个基本情况？"
>
> **客户**: "好的，请说吧。我们用的是某品牌的 ERP 系统。"
>
> **销售顾问**: "了解了。贵公司目前如何使用供应链管理系统处理订单流程？"
>
> **客户**: "主要是手动录入订单、查询库存、安排发货。系统能查到基本数据，但信息经常不及时更新。"
>
> --- **【调查阶段 — 难题问题】** ---
>
> **销售顾问**: "明白了。在处理供应链任务时，有哪些成本过高或低效的问题？"
>
> **客户**: "人工录入容易出错，经常搞错发货地址和数量。客服要打电话确认订单信息，很浪费时间。"
>
> --- **【影响阶段 — 影响问题 ⭐ 关键转化】** ---
>
> **销售顾问**: "数据延迟确实是个大问题。如果这个问题持续存在，对客户满意度有什么具体影响？"
>
> **客户**: "客户会取消订单或转向竞争对手。"
>
> --- **【价值呈现 — 需求效益问题】** ---
>
> **销售顾问**: "我理解这个影响。如果实现实时订单追踪和自动预警，对您的客户服务团队意味着什么？"
>
> **客户**: "客服人员可以专注于解决问题，而不是查订单状态。客户满意度会显著提升，订单错误率降低 90% 以上。"

---

## 💡 **快速开始示例**

### 🐍 Python（推荐）

```bash
# 1. 生成 SPIN 四阶段提问序列
python scripts/question_generator.py

# 2. 运行完整 SPIN 流程演示
python scripts/basic_demo.py

# 3. 按行业生成开场白话术
python scripts/opening.py --industry 金融科技
python scripts/opening.py --industry 医疗
```

---

### 📜 JavaScript（可选参考）

查看 [examples/](examples/) 目录获取 JS 版演示：
- [basic_usage.js](examples/basic_usage.js) - SPIN 四阶段流程完整演示
- [objection_handling.js](examples/objection_handling.js) - 客户异议处理实战技巧
- [performance-tips.md](examples/performance-tips.md) - 性能优化与最佳实践指南

---

### 🧪 运行单元测试

```bash
pip install pytest && pytest tests/ -v
```

涵盖 [test_spin_sales.py](tests/test_spin_sales.py) — `question_generator` `opening` `demo_interview` `basic_demo` 共 18 个测试用例。

---

如需总览查看，可先阅读 [README.md](README.md) 快速入门文档。

---

## 📚 **培训材料**

`training/` 目录提供 SPIN 销售法培训配套资源，适合自学和团队培训：

| 文件 | 内容概要 | 文件大小 |
|------|---------|---------|
| [spin-questions-bank.md](training/spin-questions-bank.md) | S/P/I/N 全阶段题库，按行业分类 | 23.1 KB |
| [interactive-exercises.md](training/interactive-exercises.md) | 互动练习脚本，含角色扮演场景 | 11.0 KB |
| [evaluation-checklist.md](training/evaluation-checklist.md) | 销售对话评估清单和打分标准 | 24.1 KB |

---

## 📊 **推荐资源清单**

### **📚 书籍：**

- 《SPIN Selling》- Neil Rackham (原著，必读经典)
- 《销售巨人》- SPIN 中文版译本
- 《挑战者销售》- Challenger Sale（补充方法论）
- 《顾问式销售》- 咨询式销售的延伸

### **🌐 在线资源：**

- Zendesk SPIN 销售实战指南
- Salesforce SPIN Selling 培训材料
- Shopify SPIN 问题模板库

---

## 🎓 **核心总结**

> "SPIN 不是关于推销产品，而是通过提问帮助客户发现并理解自己的需求。顶级的销售问出更多 Implication 问题，让客户自己认识到问题的严重性和解决方案的价值。"
> — Neil Rackham, SPIN Selling Book

*注：
      *本技能基于尼尔·雷克汉姆的 SPIN 销售法理论框架*
      *适用于复杂 B2B 销售场景的专业咨询*

---
