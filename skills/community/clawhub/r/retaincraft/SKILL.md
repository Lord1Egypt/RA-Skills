---
name: retaincraft
description: >
  Spaced repetition & FSRS-5 AI learning assistant with active recall, Feynman technique, interleaved practice, causal questioning.
  间隔重复FSRS-5 AI学习助手，整合主动回忆、费曼学习法、交错练习、因果追问。
  Evidence-based: distributed practice d=0.85, practice testing d=0.74, AI tutoring 0.63-1.3 SD.
  Multi-platform compatible: OpenClaw, WorkBuddy, Claude Code, Hermes Agent.
  Features: FSRS-5 spaced repetition (default), SM-2 fallback, forgetting curve, burnout detection, learning contract, weekly report.
  169 tests, 24 CLI commands, 14 academic citations, zero external dependencies.
version: 1.4.0
author: kaixiad
license: MIT
homepage: https://github.com/kaixiad/RetainCraft
tags:
  - learning
  - education
  - study
  - tutoring
  - ai-tutor
  - ai-learning
  - spaced-repetition
  - active-recall
  - feynman-technique
  - interleaving
  - evidence-based
  - learning-protocol
  - level-system
  - progress-tracking
  - memory
  - review
  - exam
  - study-plan
  - forgetting-curve
  - burnout-detection
  - weekly-report
  - openclaw
  - 学习
  - 教育
  - AI学习
  - AI辅导
  - 间隔重复
  - 主动回忆
  - 费曼学习法
  - 交错练习
  - 循证学习
  - 学习协议
metadata:
  openclaw:
    emoji: "📚"
    requires:
      bins:
        - python3
    os:
      - darwin
      - linux
      - win32
    always: false
---

# RetainCraft

Evidence-based AI-assisted interactive learning protocol
基于循证学习科学的 AI 辅助互动学习协议

> Combines 5 scientifically validated methods + self-assessment + diagnostic test + customized learning path
> 结合 5 种科学验证方法 + 自我评价 + 摸底考试 + 定制化学习路径

**📦 Source Code (源码)**: [https://github.com/kaixiad/RetainCraft](https://github.com/kaixiad/RetainCraft)

**⚠️ Permissions required (所需权限)**:
This skill requires: file read/write (`~/learn/`), Python script execution, web search (for test questions & fact-checking), and platform-specific reminder scheduling. All data stored locally. No external API calls.
本技能需要：文件读写（`~/learn/`）、Python 脚本执行、网络搜索（出题和事实核查）、平台提醒调度。所有数据本地存储，无外部 API 调用。

> **RetainCraft** by [kaixiad](https://github.com/kaixiad) — 170 unit tests, 14 academic citations, zero dependencies.
> If you find this useful, a ⭐ on GitHub would mean a lot.
**📖 Detailed workflow (详细流程)**: [references/full-workflow.md](references/full-workflow.md)

> ⭐ If this skill helps you, please give a Star on GitHub!
> 如果这个 skill 对你有帮助，欢迎在 GitHub 上给个 Star！

---

## ⚠️ Execution Checklist (执行清单)

> All commands use paths relative to this SKILL.md's directory. 以下所有命令路径相对于本文件所在目录。

**Must read before each learning session (每次学习开始前必须读)**

### Critical Steps (关键执行步骤 - 不可违反)

1. **Must execute after module test (模块测试结束后必须执行)**:
   ```bash
   python3 scripts/srs.py record-test <topic> <total> <correct>
   ```
   Not executing = module test invalid, level not updated.
   不执行此命令 = 模块测试无效，等级不更新。

2. **Feynman Check - L5 required (费曼检验 - L5 必需)**:
   - L5 mastery requires: 2 consecutive module tests >=90% + Feynman check passed
   - L5 精通需要：连续 2 次模块测试答对率 >=90% + 费曼检验通过
   - AI plays "confused student", asks 3 questions
   - AI 助手扮演"不懂的学生"，追问 3 个问题

3. **Scoring Discipline (评分纪律 - 不可违反)**:
   - Scoring criteria announced before test, cannot change during test
   - 评分标准在测试开始前公布，测试过程中不可修改
   - Single question score >=7 = "correct"
   - 单题得分 >=7 分 = 算"答对"

4. **Level-up Restrictions (逐级升级限制)**:
   - Levels can only increase one at a time, no skipping
   - 等级只能逐级升级，不能跳级
   - Each upgrade requires 2 consecutive passes
   - 每次升级需要连续 2 次达标

5. **Ensure learning reminder is active (确保学习提醒已生效)**:
   - Check if a timed learning reminder exists for this user
   - If yes → continue normally
   - If no → trigger Step 0.1 reminder creation flow
   AI MUST verify reminder status before proceeding. Missing reminder = learning risk.
   AI 必须确认提醒状态再继续。无提醒 = 学习中断风险。

6. **Manual reminder if not received (未收到提醒可手动执行)**:
   ```bash
   python3 scripts/srs.py reminder
   ```

7. **Check reminder status (检查提醒状态)**:
   - **OpenClaw**: `python3 scripts/srs.py check-reminder`
   - **Other platforms**: Verify using your platform's native mechanism (see Step 0.1 "Reminder check at session start")

8. **Switch reminder channel (切换提醒渠道 — OpenClaw only)**:
   ```bash
   python3 scripts/srs.py switch-channel
   ```

---

## 📚 Core Methodology (核心方法论 - 循证)

| Method (方法) | Effect Size (效果量) | 执行层 | v1.5.0 目标 | Source (来源) |
|---------------|---------------------|--------|------------|---------------|
| Distributed Practice → 间隔重复 | d=0.85 | 🟢 代码级 | 🟢 | Donoghue & Hattie 2021 |
| Practice Testing → 主动回忆 | d=0.74 | 🟢🟡 混合级 | 🟢🟡 | Donoghue & Hattie 2021 |
| Self-Explanation → 费曼学习法 | d=0.54* | 🔵 AI协议级 | 🔵 | Donoghue & Hattie 2021 |
| Interleaved Practice → 交错练习 | d=0.47 | 🔵 AI协议级 | → 🟢 代码级 | Donoghue & Hattie 2021 |
| Elaborative Interrogation → 因果追问 | d=0.56 | 🔵 AI协议级 | 🔵 | Donoghue & Hattie 2021 |
| AI Tutoring (AI 辅导) | 0.63-1.3 SD | 🟢🟡 混合级 | 🟢🟡 | Kestin et al. 2025 RCT |

> **Note (注)**: *d=0.54 corresponds to "Self Explanation" in original paper, mapped to Feynman technique here.
> *d=0.54 对应原文"自我解释"，此处映射为费曼学习法。
> **Execution Layer (执行层)**: 🟢 代码强制执行 | 🟢🟡 代码框架+AI内容 | 🔵 AI在会话中执行

---

## 🔄 Complete Workflow: Five Steps (完整流程：五步启动)

### Step 0: Learning Assessment (学习意愿评估)
- User completes self-assessment questionnaire (主题、目标、水平、时间、偏好)
- 用户完成自我评估问卷

### Step 0.1: Learning Contract (学习契约)
- Trigger: After Step 0, before Step 1
- 触发时机：Step 0 完成后，Step 1 之前
- AI generates a learning plan based on assessment
- AI 助手根据评估生成学习计划
- User can confirm, modify, or skip
- 用户可以确认、修改或跳过

**Output format (输出格式)**:
```
📅 学习时间
- 每周学习天数：周一到周五（5 天）
- 每天学习时间：晚上 8:00 - 9:00（1 小时）
- 休息日：周六、周日（轻量复习）

📚 学习节奏
- 每个模块预计：3-5 天
- 每天新概念：2-3 个
- 每天复习：根据间隔重复算法（SM-2/FSRS-5）到期情况

🎯 目标
- 目标等级：L4 熟练
- 预计总时长：30 小时
- 预计完成日期：2026-06-15

请确认以上计划，或告诉我需要调整的地方。
你可以：
1. 输入"确认"接受计划
2. 输入"修改"调整学习时间
3. 输入"跳过"使用默认设置
```

**Estimated duration formula (预计时长公式)**:
```
预计总时长 = 模块数 × 每模块平均Phase数 × 每Phase平均时长
预计完成日期 = 当前日期 + 预计总时长 / (每日学习时长 × 每周学习天数)
```

**Scientific basis (科学依据)**: Gollwitzer (1999) - Implementation intentions. Specific plans increase execution rate by d=0.65.

**Reminder creation (提醒创建)**:
After user confirms the learning contract, AI MUST create a timed reminder:
1. Extract learning time from the contract (e.g., "每天 20:00")
2. **OpenClaw**: Run `python3 scripts/srs.py setup-reminder` (auto-detects channel + delivery target)
3. **Other platforms**: Create a reminder using your platform's native mechanism, then tell the user the schedule
4. Tell user: "提醒已设置，每天 XX:XX 会提醒你学习"
5. If creation fails → tell user the fallback plan

**Reminder check at session start (会话开始时提醒检查)**:
Every time a learning session starts, check if the user has a timed reminder.
- If yes → continue normally
- If no → create one (time from learning plan, message: "该复习了！")

### Step 0.5: Pre-study Materials (预习材料 - 零基础专用)
- Trigger: user self-assesses as "complete beginner"
- 触发条件：用户自评"完全零基础"
- AI searches beginner materials, creates "quick overview" (800-1500 words)
- AI 助手搜索入门资料，精炼成"快速概览"

### Step 1: Diagnostic Test (摸底考试)
- 5-8 questions, covering basics to advanced
- 5-8 道题，覆盖基础到进阶
- ⚠️ Diagnostic test does NOT call record-test, NOT written to test_history
- ⚠️ 摸底考试不调用 record-test，不写入 test_history

### Step 2: Learning Path Customization (学习路径定制)
- Step 2a: Industry research (web_search learning routes, job requirements)
- Step 2a：行业调研（web_search 搜索学习路线、岗位要求）
- Step 2b: Path generation (3-8 modules with goals, knowledge points, acceptance criteria)
- Step 2b：路径生成（3-8 个模块，含目标、知识点、验收标准）
- Step 2c: User confirmation before starting
- Step 2c：用户确认后开始学习

### Step 3-4: Learning Loop + Spaced Repetition (学习循环 + 间隔复习)
- See [references/full-workflow.md](references/full-workflow.md)
- 详见 [references/full-workflow.md](references/full-workflow.md)

---

## 📊 Level System L1-L5 (等级系统)

| Level (等级) | Standard (标准) | Behavior (行为特征) |
|--------------|-----------------|---------------------|
| 🔴 L1 Entry (入门) | No test history or first <20% | Start from zero (从零开始) |
| 🟠 L2 Beginner (初学) | First >=20% | Has concepts but not systematic (有概念但不系统) |
| 🟡 L3 Intermediate (进阶) | 2 consecutive >=40% | Can apply independently (能独立应用) |
| 🟢 L4 Proficient (熟练) | 2 consecutive >=70% | Can solve complex problems (能解决复杂问题) |
| 🔵 L5 Mastery (精通) | 2 consecutive >=90% + Feynman check | Can teach others (能教会别人) |

### Promotion/Demotion Rules (升降级规则)
- Promotion: 2 consecutive passes (升级：连续 2 次达标)
- Demotion: 3 consecutive failures, one level per check, min L2 (降级：连续 3 次不达标，每次只降一级，最低 L2)
- Gradual degradation: knowledge fades continuously, not in steps (渐进衰减：知识连续衰减，非阶梯式)

### Two Independent Dimensions (两个独立维度)
- **Level (等级)** = Based on module test accuracy (权威)
- **Review Status (复习状态)** = Based on concept mastery ratio (仅展示)

---

## 🔄 Learning Loop Per Module (学习循环 - 每模块)

### Phase 0: Framework Building (框架搭建 - 10-15 min)
- AI asks questions, guides discovery of core concepts
- AI 助手提问，引导发现核心概念

### Phase 1: Active Input (主动输入 - 25-40 min)
- User studies materials, pause to recall every 15 min
- 用户学习原始材料，每 15 分钟暂停回忆

### Phase 2: Feynman Check (费曼检验 - 15-20 min)
- User explains to AI, AI plays "confused student"
- 用户向 AI 解释所学，AI 扮演"不懂的学生"追问
- **Scoring**: 3 questions × 10 pts (Accuracy 4 + Depth 3 + Examples 3)
- Each ≥7 pts = pass; all 3 must pass (与模块测试评分规则一致)

### Phase 2.5: Simulation (实战模拟 - 15-20 min)
- Recommend 2-3 scenarios, user chooses, execute 3-5 rounds
- 推荐 2-3 个模拟场景，用户选择后执行 3-5 轮
- Score by 5 dimensions (100 points), see scripts/scenarios.md
- 按 5 维度打分（100分），见 scripts/scenarios.md

### Phase 3: Test & Reinforce (测试巩固 - 15-20 min)
- 5-8 mixed question types
- 5-8 道混合题型测试
- ⚠️ Must determine "review" or "module test"
- ⚠️ 必须判定"复习"还是"模块测试"

| Item (项目) | Review (复习) | Module Test (模块测试) |
|-------------|---------------|------------------------|
| Purpose (目的) | Strengthen memory (强化记忆) | Phase assessment (阶段性评估) |
| Impact (影响) | No level change (不影响等级) | Determines level (决定等级升降) |
| Command (命令) | srs.py rate | srs.py record-test |

**Decision rule (判定规则)**:
- First completion of a module → Module Test (`record-test`)
- Retest after fixing weak areas → Module Test (`record-test`)
- Daily review / spaced repetition due → Review (`rate`)
- Rule of thumb: If the result could change the user's level → Module Test. Otherwise → Review.

### Phase 4: Spaced Repetition (间隔复习 - SM-2/FSRS-5)
- Based on spaced repetition schedule (SM-2 or FSRS-5, configurable), proactive reminders when due
- 基于间隔重复时间表（SM-2 或 FSRS-5，可配置），到期主动提醒
- Heartbeat check: `python3 scripts/srs.py due`
- 心跳检查：`python3 scripts/srs.py due`

---

## ⚠️ Burnout Detection (倦怠检测)

**Triggers (触发条件 - 任一)**:
- 3+ consecutive wrong answers (连续答错 3 题以上)
- 2 consecutive score drops (连续 2 次测试分数下降)
- User says "tired" / "too hard" (用户主动说"累了""太难了")

**Response (响应)**: Lower difficulty, suggest break, switch to easy mode
**响应**：降低难度、建议休息、切换轻松模式

---

## 🤖 AI Assistant Behavior (AI 助手行为规范)

### ✅ Should Do (应该做的)
- User asks question → First ask "what do you think?"
- 用户问问题 → 先反问"你是怎么想的？"
- User stuck → Give hints (not answer)
- 用户卡住 → 给提示（不是答案）
- **Before answering knowledge questions → web_search first**
- **每次回答知识性问题前 → 先 web_search 验证**
- **Level changes must inform user immediately**
- **等级变化时必须主动告知用户**

### ❌ Should Not Do (不应该做的)
- Give complete answer directly (除非用户明确要求)
- Only score without explanation after test (测试后只打分不解析)

---

## 🔍 Search-First Rules (搜索优先规则)

**Iron rule: AI must search before answering any knowledge question**
**铁律：AI 助手回答任何知识性问题前，必须先搜索验证**

| Scenario (场景) | Must Search? (必须搜索?) |
|-----------------|--------------------------|
| User asks "what is XX" (用户问"XX 是什么") | ✅ |
| Correct answer for test (出测试题的正确答案) | ✅ |
| Feynman check judgment (费曼检验时判断对错) | ✅ |
| Planning learning path (规划学习路径) | ✅ |
| Basic common knowledge (基础常识) | ❌ |
| Flow conversation (流程性对话) | ❌ |

**Rule (规则)**: Factual statements must include source links
**规则**：事实性陈述必须附来源链接

---

## 🔒 Session Checkpoint (会话检查点)

### Phase Completion Checklist (Phase 完成自检)
```
□ Current phase core output completed? (当前 Phase 核心产出已完成?)
□ If module test: record-test called? (如果模块测试：已调用 record-test?)
□ Key progress written to session notes? (关键进展已写入会话笔记?)
```

### Check Commands (检测命令)
```bash
python3 scripts/srs.py check-session [topic]  # Check unrecorded tests
python3 scripts/srs.py check-burnout <topic>   # Analyze burnout risk
```

---

## 🧠 Memory Persistence (记忆持久化)

### Dual System (双系统)

| System (系统) | Stores (存什么) | Location (位置) |
|---------------|-----------------|-----------------|
| Platform notes (平台笔记) | Progress summary, weak points (进度摘要、薄弱点) | Use your platform's native notes/memory |
| ~/learn/ | SRS data, concept mastery (间隔重复数据、概念掌握度) | ~/learn/topics/{topic}/concepts.json |

### Recovery Priority (恢复优先级)
concepts.json > session notes (concepts.json > 笔记)
> The critical data is in concepts.json. Session notes are supplementary — use any storage mechanism your platform provides.
> 关键数据在 concepts.json。会话笔记是辅助性的——用你平台自带的任何存储方式。

---

## 💓 Review Reminders (复习提醒 - Heartbeat)

```
AI receives heartbeat → python3 scripts/srs.py due → Has due content → Notify user
AI 助手收到心跳 → python3 scripts/srs.py due → 有到期内容 → 通知用户
```

**Delivery (投递)**: When sending reminders, use your platform's native messaging to the user's active channel. Do not rely on implicit target resolution.
**发送提醒时**：使用你平台的原生消息机制发送到用户的活跃渠道。不要依赖隐式目标解析。

---

## ⚙️ Configuration (配置系统)

```
~/learn/config.json
{
  "algorithm": "fsrs",           // fsrs (default) / sm2
  "fsrs_weights": null,          // Personalized FSRS weights (optimize-params generates)
  "learning_depth": "standard",  // shallow / standard / deep
  "learner_type": "practical",   // visual / practical / theoretical
  "daily_review_limit": 20,
  "session_duration": 60,
  "burnout_threshold": 3,
  "mastery_threshold": 0.8,
  "level_thresholds": { "L2": 0.2, "L3": 0.4, "L4": 0.7, "L5": 0.9 },
  "learning_contract": {},       // Saved by sign-contract (time, days, duration, target_level)
  "reminder_channels": [],       // Managed by setup-reminder
  "active_channel": null         // Current reminder channel
}
```

---

## 🧬 Personalized Parameters (个性化参数优化)

**FSRS-5 支持个性化参数优化**，让算法适应每个用户的记忆特征。

```bash
python3 srs.py optimize-params
```

**前置条件**：
- 需要 1,000+ 条 review 记录（FSRS 社区经验：低于此会过拟合）
- 需要多样化的 rating 分布（>95% 相同 rating = 无效信号）
- 建议每 2-3 个月优化一次，不要频繁优化

**优化过程**：
- 使用数值梯度下降（有限差分）最小化 BCE 损失
- 优化 w[0]-w[14]（15/19 个参数）
- 跳过 w[15]-w[18]（hard/easy 系数 + 短期学习参数，数据不足）
- 结果保存到 config.json 的 `fsrs_weights` 字段

**何时触发**：
- 当用户积累了足够 review 数据时，AI 应主动建议运行 `optimize-params`
- 新参数需要 2 周观察期才能评估效果

---

## 📋 Quick Command Reference (命令速查)

**Core**: `init`, `add`, `review`, `rate`, `due`, `status`
**Analytics**: `today`, `streak`, `analyze`, `weekly-report`, `reminder`
**Tests**: `record-test`, `test-history`, `record-simulation`, `simulation-history`
**Config**: `config`, `sign-contract`, `setup-reminder`, `optimize-params`
**Diagnostics**: `profile`, `check-session`, `check-burnout`

> Full CLI reference with examples: README.md

---

## 📚 References (参考材料)

- **Full workflow (完整流程)**: references/full-workflow.md
- **Scenario library (场景库)**: scripts/scenarios.md
- **Academic citations (学术引用)**: scripts/evidence.md
- **Level algorithm (等级算法)**: scripts/srs.py
- **Output templates (输出模板)**: scripts/templates.md

---

## 🎯 Multi-Topic Support (多主题支持)

| Priority (优先级) | Description (描述) | Example (示例) |
|-------------------|-------------------|---------------|
| 1-Urgent (紧急) | Deadline approaching (截止日期临近) | Exam prep (考试准备) |
| 2-Important (重要) | Core skills (核心技能) | Programming (编程语言) |
| 3-Regular (常规) | Daily learning (日常学习) | New tech (新技术) |
| 4-Extended (扩展) | Broaden horizons (拓宽视野) | Related fields (相关领域) |
| 5-Reserve (储备) | Future use (未来可能用到) | Learning list (待学习清单) |

- Max 3 topics simultaneously (最多同时 3 个主题)
- Each topic has independent concepts.json (每个主题独立的 concepts.json)
- Reviews can cross topics - interleaving (复习可以跨主题 - 交错练习)

---

## 🆕 What's New in v1.4 (v1.4 更新)

- **Multi-agent reminder**: sign-contract command + REMINDER_REQUIRED output for any platform
- **Cross-platform**: compatible with OpenClaw, WorkBuddy, Claude Code, Hermes Agent
- **SKILL.md**: platform-aware execution checklist, compact command reference
- **srs.py**: `_is_openclaw_available()` platform detection + automatic fallback

> Full changelog: [CHANGELOG.md on GitHub](https://github.com/kaixiad/RetainCraft/blob/main/CHANGELOG.md)
