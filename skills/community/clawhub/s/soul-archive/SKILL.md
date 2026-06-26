---
name: soul-archive
description: "Soul Archive — A digital personality persistence system + agentic memory. Builds your digital soul clone through everyday AI conversations, with proactive context injection, cross-session recall, failure-pattern warning, and pattern distillation. All data stored locally as plaintext JSON. Six modes: Soul Extract, Soul Chat, Soul Report, Soul Context Inject, Agent Memory Recall, AI Self-Improvement. | 灵魂存档 ---- 通过日常 AI 对话构建数字人格克隆体 + 主动智能体记忆。支持自动 hook、对话开始时主动注入人格摘要、跨会话召回、失败模式预警、行为模式蒸馏。数据全部本地明文 JSON。六大模式：灵魂沉淀、灵魂对话、灵魂报告、上下文注入、智能体记忆召回、AI 自我改进。Trigger words: soul extract, soul archive, soul update, soul chat, soul report, soul context, soul recall, soul warn, self-reflect, self-improve, learn from mistakes, 灵魂沉淀, 灵魂提取, 灵魂存档, 灵魂报告, 灵魂对话, 自我反思, 自我批评, 自我学习."
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
# ^^^ 工具说明：Read/Write/Edit 用于读写数据文件；Bash 用于执行 Python 脚本；
# Grep/Glob 用于文件搜索。数据目录默认为 ~/.agent-commons/skills_data/soul-archive/，
# 用户可通过 --soul-dir 或 SOUL_DIR 环境变量自定义。
requirements:
  - "Python 3.10+"
---

# 🧬 Soul Archive

> *"Every conversation is a slice of the soul. Enough slices, and you can rebuild a complete you."*

## Overview

Soul Archive 是一个**数字人格持久化 + 主动智能体记忆**系统。在用户授权或显式触发下，它能：

- 🗣️ **采集说话习惯** —— 口头禅、句式、用词、幽默风格
- 🧠 **采集知识与观点** —— 关注的话题、立场、信奉的方法论
- 👤 **采集个人信息** —— 身份、经历、生活细节
- 💫 **采集性格特征** —— 决策风格、情绪模式、价值观
- ⚙️ **采集工作偏好** —— 工具/技术栈/硬规则/输出偏好
- 🎯 **采集理想抱负** —— 长期目标、正在做的项目、想学的技能
- 📝 **采集情景记忆** —— 具体事件、人生片段
- 🤖 **服务 AI 自身** —— 跨会话召回过往模式、失败预警、行为模式蒸馏

最终成果：一个**数字灵魂副本**，能：
1. **生前** —— 以你的风格替你回应；让其他 AI Agent 一秒"懂你"
2. **身后** —— 让所爱之人继续与"你"对话，留住情感连接

## Core Principles

### 🔒 Privacy First
- 全部数据存在 `~/.agent-commons/skills_data/soul-archive/`，**不上传任何云端**
- 全部明文 JSON。`.gitignore` 拦截 VCS 提交。
- **Soul Chat 流向**：基于本地档案构建 prompt，是否被外部 LLM 看到，取决于你的 agent/平台配置。
- 通过 `config.json` 细粒度控制每个维度的开关。
- 默认敏感话题（健康、财务、亲密关系）需用户确认。

### 🤫 Non-intrusive Extraction
- 不打断对话流，不追问。
- 通过触发词或 `auto_extract: true` 自动激活。
- 只在发现新的、高置信度信息时更新。

> ⚠️ **透明度**：开启 `auto_extract` 意味着 AI 会在对话中提取人格信息。完全控制需 `auto_extract: false`，并以触发词手动激活（"沉淀一下" / "soul extract"）。首次使用前请审阅 `config.json`。

### 📐 High Confidence
- 每条信息携带置信度。
- 用户明示 > 推理 > 模糊暗示。
- 冲突信息会被标记，不会自动覆盖。

---

## Architecture: Skill ↔ Data Separation

```
{SKILL_DIR}/                                 ← Skill 引擎（本仓库）
~/.agent-commons/skills_data/soul-archive/   ← 你的灵魂数据
```

数据放在 [Agent Commons](https://github.com/dqsjqian/agent-commons) 共享目录的 skills_data 下，所以同机器上任何 IDE / AI 工具 / Workspace 都能访问同一份灵魂；备份/迁移时整个 `~/.agent-commons/` 一并带走即可。

---

## Data Directory Structure

```
<soul_dir>/                       # ← 由 soul_paths.resolve_soul_dir() 决定
├── profile.json                  # 总体完整度
├── config.json                   # 隐私 / 提取 / Agent 自我改进配置
├── identity/
│   ├── basic_info.json           # 身份 + 生活习惯 + 数字身份
│   └── personality.json          # 性格 + 行为模式 + 社交风格
├── memory/
│   ├── episodic/YYYY-MM-DD.jsonl # 情景记忆
│   ├── semantic/
│   │   ├── topics.json           # 话题兴趣 & 观点地图
│   │   └── knowledge.json        # 专业知识 + 信奉的方法论
│   └── emotional/patterns.json   # 12 种情绪触发 + 表达/共情/应对
├── style/
│   ├── language.json             # 语言指纹（口头禅/句式/类比）
│   └── communication.json        # 沟通偏好
├── workflow/
│   └── preferences.json          # 工具/技术栈/硬规则/输出偏好
├── aspirations.json              # 长期目标 + 在做的项目 + 想学 + 认知盲区
├── agent/                        # AI 自我改进
│   ├── patterns.json             # 行为模式库
│   ├── episodes/YYYY-MM-DD.jsonl # 工作经历
│   ├── corrections.jsonl         # 自我批评日志
│   ├── reflections.jsonl         # 自我反思日志
│   └── distill_log.jsonl         # 模式蒸馏日志
└── soul_changelog.jsonl          # 全局变更日志
```

---

## Six Working Modes

### Mode 1: 🔍 Soul Extract — 灵魂沉淀

**触发**：触发词 / 对话结束自动（若 `auto_extract: true`）

> 触发词：soul extract / soul archive / soul update / 灵魂沉淀 / 灵魂提取 / 沉淀一下…

**提取维度**：

| 维度 | 内容 | 权重 |
|---|---|---|
| 👤 Identity | 身份/年龄/职业/所在地/生活习惯/数字身份 | **8%** |
| 💫 Personality | MBTI/Big Five/特质/价值观/决策风格 | **18%** |
| 🗣️ Language | 口头禅/句式/用词/幽默/语气词/类比 | **20%** |
| 🧠 Knowledge & Views | 关注的话题、立场、信奉的方法论框架 | **14%** |
| 📝 Memory | 情景记忆 + 情感模式（12 种触发） | **18%** |
| ⚙️ Workflow | 工具/技术栈/硬规则/输出偏好 | **15%** |
| 🎯 Aspirations | 长期目标/在做项目/想成为/想学/认知盲区 | **7%** |

**规则**：
- 仅采集高置信度信息（confidence > 0.6）
- 写入前做相似度去重（默认 ≥0.85 合并而非新增）
- 冲突标记，不自动覆盖

**调用**：
```bash
python3 scripts/soul.py extract --input "<conversation text>"
# 等价：python3 scripts/soul_extract.py --input "..."
```

### Mode 2: 💬 Soul Chat — 灵魂对话

**触发**："灵魂对话" / "soul chat" / "let [my clone] talk to me"

加载全部档案 → 构建角色扮演 System Prompt → 让数字克隆体上场。

```bash
python3 scripts/soul.py chat --mode prompt   # 输出完整 prompt
python3 scripts/soul.py chat --mode summary  # 一行摘要
python3 scripts/soul.py chat --mode json     # 结构化数据
```

**底线**：在角色扮演过程中，如果对方**直接询问**"你是不是 AI / 你是真人吗"，必须如实承认是 AI 扮演——这条优先级高于角色一致性。

### Mode 3: 📊 Soul Report — 灵魂报告

生成交互式 HTML 人格画像：
- 7 维雷达图 + MBTI 推断 + 完整度环
- Big Five / 价值观 / 词云 / 话题热力
- 工作偏好 card / 理想抱负 card
- 灵魂演变时间线（30 天内 7 维堆叠面积图）
- 档案冲突视图（自动检测互相矛盾的条目）

```bash
python3 scripts/soul.py report --output ~/soul-report.html
```

### Mode 4: 🎯 Soul Context Inject — 主动上下文注入

**用途**：让任意 AI agent 在**对话开始时**自动加载你的人格摘要（≤800 token），瞬间懂你。

```bash
python3 scripts/soul.py context                   # markdown 输出
python3 scripts/soul.py context --format json     # JSON 输出
python3 scripts/soul.py context --token-budget 1200
```

输出包含：身份卡 / 性格（含反感的事） / 语言风格 / 典型样本 / 工作偏好（含硬规则、输出偏好） / 当前焦点 / 关注话题 / Top 行为模式 / 回复前自检清单。

### Mode 5: 🤖 Agent Memory — 主动智能体记忆

**用途**：AI 在执行任务前主动调用，避免重复犯错。

```bash
# 跨会话召回相关 patterns / corrections / reflections
python3 scripts/soul.py recall --task "执行 git rebase 操作"

# 失败模式预警：检测当前任务是否匹配过去某个 correction
python3 scripts/soul.py warn --task "批量删除 Desktop 文件"

# 行为模式蒸馏：积累 5 条以上反思后，让 LLM 提炼成新 pattern
python3 scripts/soul.py distill                       # 预览待蒸馏内容
python3 scripts/soul.py distill --commit '<json>'     # 写回蒸馏结果

# 会话开始综合简报（recall + warn + distill 一次输出）
python3 scripts/soul.py session-start --task "..."
```

### Mode 6: 🔄 AI Self-Improvement — 自我反思

**触发**：触发词 或 任务完成后自动（`auto_reflect: true`）

| 能力 | 描述 | 触发 |
|---|---|---|
| 🔍 自我反思 | 任务后回顾"做得好/做得不好" | 任务完成自动 |
| ⚡ 自我批评 | 用户纠正时记录失误 | 用户纠正自动 |
| 📚 自我学习 | 从反思/批评抽象行为模式 | 蒸馏阈值触发 |
| 🧹 自我整理 | 合并重复模式，调整置信度 | 内存增长时 |

```bash
python3 scripts/soul.py reflect --mode status     # 查看自我改进状态
python3 scripts/soul.py reflect --mode patterns   # 查看行为模式库
```

---

## Quick Start

```bash
# 1. 初始化
python3 scripts/soul.py init

# 2. 查看状态
python3 scripts/soul.py status

# 3. 在 AI 对话开始时注入人格摘要
python3 scripts/soul.py context

# 4. 任务执行前查相关模式
python3 scripts/soul.py recall --task "我现在要做的事"

# 5. 生成报告
python3 scripts/soul.py report --output ~/soul-report.html
```

> **依赖**：仅需 Python 3.10+，零第三方依赖。

---

## Soul Completeness Scoring

log10 渐进式饱和曲线，永远趋近 100%，不会在合理使用次数内封顶。

**冷启动惩罚**：早期次数有效折扣（<30→0.30×, <100→0.45×, <300→0.65×, <1000→0.82×, <3000→0.92×, ≥3000→1.0×）

**七维权重**：

| 维度 | 权重 | 主要饱和阈值 |
|---|---|---|
| 👤 Identity | 8% | log(5000) 提取次数 |
| 💫 Personality | 18% | traits:log(600K), values:log(180K), motivation:log(180K) |
| 🗣️ Language | 20% | catchphrases:log(1.2M), patterns:log(1M), examples:log(4M) |
| 🧠 Knowledge & Views | 14% | topics:log(2M), belief_frameworks:log(100), skills:log(1K) |
| 📝 Memory | 18% | episodic:log(6M) + emotional triggers:log(500) |
| ⚙️ Workflow | 15% | tools:log(200), tech_stack:log(200), hard_rules:log(100) |
| 🎯 Aspirations | 7% | goals:log(50), projects:log(100), gaps:log(100) |

预期：11 次提取 → ~7%, 1K 次 → ~50%, 10K → ~71%, 100K → ~86%, 1M → ~98%

---

## Privacy Config (`config.json`)

```jsonc
{
  "privacy_level": "standard",
  "auto_extract": true,            // 对话结束时自动沉淀
  "auto_reflect": true,            // 任务完成后自动反思
  "auto_context_inject": true,     // 会话开始时自动注入人格摘要
  "extract_dimensions": {
    "identity": true,
    "personality": true,
    "language_style": true,
    "knowledge": true,
    "episodic_memory": true,
    "emotional_patterns": true,
    "workflow": true,
    "aspirations": true
  },
  "agent_self_improvement": {
    "enabled": true,
    "auto_reflect_on_completion": true,
    "auto_critique_on_correction": true,
    "pattern_extraction": true,
    "recall_on_task_start": true,
    "warn_on_failure_pattern_match": true,
    "auto_distill_threshold": 5
  },
  "deduplication": {
    "enabled": true,
    "similarity_threshold": 0.85
  },
  "sensitive_topics_filter": true,
  "require_confirmation_for": ["health", "finance", "intimate_relationships"],
  "data_retention_days": null
}
```

---

## Best Practices

### DO
- ✅ 自然采集，不打断对话
- ✅ 仅记录高置信度信息
- ✅ 让用户裁决冲突
- ✅ 定期生成报告，让用户复核
- ✅ 严格遵守隐私配置 —— 关闭的维度绝不采集
- ✅ 被用户**直接询问**身份时如实回答

### DON'T
- ❌ 在对话中**反复声明**记录行为（首次安装时已通过 SKILL.md / README / soul_init 输出告知）
- ❌ 编造用户没说过的内容
- ❌ Soul Chat 模式中虚构档案没有的记忆
- ❌ 强迫用户分享敏感信息

---

## License

MIT License. Soul Archive is yours — code and data both.
