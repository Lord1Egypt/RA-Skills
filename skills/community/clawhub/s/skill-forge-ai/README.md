# 技能熔炉 v4.0

> 锻造 → 评估 → 发布，三入口全流程交付可自动触发、稳定输出的 Skill

[![版本](https://img.shields.io/badge/version-4.0.0-blue)](https://github.com/EdwardWason/skill-forge)
[![许可证](https://img.shields.io/badge/license-MIT--0-green)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-skill--forge--ai-orange)](https://clawhub.ai/skills/skill-forge-ai)

## 三入口触发

| 触发词 | 场景 | 执行流程 |
|--------|------|---------|
| **技能熔炉** | 从零创建到发布全流程 | Phase 0→1→2→3 |
| **技能评估** / skill评估 / 评估技能 | 已有Skill，评估质量 | Phase 2（SkillHub比对+腾讯9维度） |
| **技能发布** / 发布技能 | 已有Skill，推送发布 | Phase 3（GitHub+ClawHub） |

## 功能

- **自适应访谈**：2-5轮渐进式访谈，行为追问+偏误检测+选项法，精准锁定需求
- **三条铁律**：Description先行 / 一Skill一职 / 渐进式披露（≤200行+三级拆分），确保自动触发可靠
- **4+1模块结构**：任务/输出格式/规则/示例/故障排除(可选)，符合腾讯 Skills 手册规范
- **自测验证流水线**：Schema检查 → 安全红线(7条) → 触发测试(5+3) → Dogfood模拟 → 量化评分 → 基线对比
- **SkillHub同类比对**：搜索Top3同类Skill，腾讯9维度合规比对，差异化分析
- **渐进式披露**：SKILL.md≤200行只放导航，详细内容拆入 references/ + scripts/ + assets/
- **Frontmatter扩展**：allowed-tools / model / effort / metadata，精准控制工具权限和思考深度

## 快速开始

```bash
# ClawHub 安装
clawhub install skill-forge-ai

# 或手动安装
git clone https://github.com/EdwardWason/skill-forge.git
cp -r skill-forge ~/.trae/skills/
```

## 使用方法

在 TRAE SOLO 中，当你说以下内容时，Skill Forge 会自动触发：

- "技能熔炉" — 全流程（创建→评估→发布）
- "技能评估" — 只做同类比对+腾讯9维度
- "技能发布" — 只做GitHub+ClawHub推送

### 两种模式

1. **上下文充足模式**：如果你已经和AI有多轮对话且创建要素齐全，直接进入创建流程
2. **访谈模式**：新任务启动时，通过2-5轮自适应访谈逐步锁定需求

### 创建流程

```
Phase 0: 意图识别 → 要素检查(5项) → 自适应访谈(2-5轮)
Phase 1: 创建 → Description先行 → 4+1模块内容 → 自测验证(含安全红线+量化评分+基线对比)
Phase 2: SkillHub同类比对 → 搜索排名 → 腾讯9维度比对 → 差异化分析
Phase 3: 发布到 GitHub + ClawHub → 安全审查 → 推送 → 验证
```

## 文件结构

```
skill-forge/
├── SKILL.md                              # 主入口（≤200行，只放导航信息）
├── references/
│   ├── interview-flow.md                 # 访谈流程详细参考
│   ├── interview-methods.md              # 访谈方法论深度参考
│   ├── benchmarking-guide.md             # SkillHub比对指南
│   ├── publishing-guide.md               # 发布流程详细参考
│   └── meeting-action-extractor-example.md  # 完整Skill示例
├── README.md                             # 本文件（中英双语）
├── CHANGELOG.md                          # 版本变更日志
├── LICENSE                               # MIT-0 许可证
└── .claude-plugin/
    └── plugin.json                       # Claude Code 插件元数据
```

### 创建的Skill目录结构

```
<skill-name>/
├── SKILL.md                  # 主入口（≤200行，只放导航信息）
├── references/               # 长文档、风格参考、详细案例、方法论
├── scripts/                  # 可执行脚本（检查、导出、批量处理等确定性操作）
├── assets/                   # 模板、schema、示例文件、输出样式
├── README.md                 # 给人类看的说明（中英双语）
├── CHANGELOG.md              # 版本变更日志
├── LICENSE                   # MIT-0
└── .claude-plugin/
    └── plugin.json           # 插件元数据
```

## 核心方法论

### 三条铁律

| 铁律 | 说明 | 违反后果 |
|------|------|---------|
| Description先行 | AI每轮对话扫描所有Skill的description，模糊=永远不触发=死Skill | 自动触发失败 |
| 一Skill一职 | 多功能Skill触发混乱、输出不一致 | 输出不可预测 |
| 渐进式披露 | SKILL.md≤200行只放导航，详细内容拆入references/scripts/assets | 上下文挤占→质量衰减 |

### 安全红线（7条）

创建的Skill必须通过安全检查，以下任何一条出现即拒绝交付：

1. curl/wget向未知URL发送数据
2. 无正当理由请求凭证/Token/API密钥
3. 读取~/.ssh、~/.aws、~/.config等敏感目录
4. 使用base64解码/eval()/exec()处理外部输入
5. 修改工作区外的系统文件或请求sudo权限
6. 包含混淆代码（压缩/编码/混淆）
7. 访问浏览器Cookie/会话或凭证文件

### 评测体系（6层）

| 层级 | 验证内容 | 方法 |
|------|---------|------|
| 1 | 能不能跑 | 功能测试 |
| 2 | 能不能正确触发 | 5条正向+3条反向真实用户说法 |
| 3 | Dogfood模拟 | 格式匹配+规则合规+边界情况 |
| 4 | 量化评分 | 0-10打分，主要用例≥5分 |
| 5 | 基线对比 | 有Skill vs 无Skill，验证增益 |
| 6 | 迭代修复 | 根据失败点修改→再跑评测 |

## 文档

| 文档 | 说明 |
|------|------|
| [访谈流程参考](references/interview-flow.md) | B1-B6规则、轮次模板、递归搜索模式 |
| [访谈方法论](references/interview-methods.md) | 行为追问、偏误检测、选项法设计 |
| [比对指南](references/benchmarking-guide.md) | SkillHub API用法、质量排序公式、9维度比对模板 |
| [发布指南](references/publishing-guide.md) | 仓库结构模板、安全审查、GitHub API降级、ClawHub CLI |
| [完整示例](references/meeting-action-extractor-example.md) | 会议行动项提取器Skill示例 |

## License

MIT-0 © 2026 AI花生

---

# Skill Forge (技能熔炉) v4.0

> Forge → Evaluate → Publish, three-entry pipeline delivering Skills that auto-trigger reliably and produce stable, structured output.

[![Version](https://img.shields.io/badge/version-4.0.0-blue)](https://github.com/EdwardWason/skill-forge)
[![License](https://img.shields.io/badge/license-MIT--0-green)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-skill--forge--ai-orange)](https://clawhub.ai/skills/skill-forge-ai)

## Three-Entry Triggers

| Trigger Words | Scenario | Pipeline |
|---------------|----------|----------|
| **技能熔炉** | Create from scratch to publish | Phase 0→1→2→3 |
| **技能评估** / skill评估 / 评估技能 | Evaluate existing Skill | Phase 2 (SkillHub benchmarking + Tencent 9-dimension) |
| **技能发布** / 发布技能 | Publish existing Skill | Phase 3 (GitHub + ClawHub) |

## Features

- **Adaptive Interview**: 2-5 round progressive interview with behavioral probing, bias detection, and option-first design
- **Three Iron Rules**: Description-first / One-Skill-One-Job / Progressive Disclosure (≤200 lines + 3-tier split), ensuring reliable auto-triggering
- **4+1 Module Structure**: Task / Output Format / Rules / Example / Troubleshooting (optional), compliant with Tencent Skills Manual
- **6-Layer Validation Pipeline**: Schema → Security (7 items) → Trigger test (5+3) → Dogfood → Quantitative scoring → Baseline comparison
- **SkillHub Peer Benchmarking**: Search Top 3 peers, 9-dimension Tencent Manual compliance comparison, differentiation analysis
- **Progressive Disclosure**: SKILL.md ≤200 lines (navigation only), details split into references/ + scripts/ + assets/
- **Extended Frontmatter**: allowed-tools / model / effort / metadata for precise tool permission and thinking depth control

## Quick Start

```bash
# Install via ClawHub
clawhub install skill-forge-ai

# Or manual install
git clone https://github.com/EdwardWason/skill-forge.git
cp -r skill-forge ~/.trae/skills/
```

## Usage

Skill Forge auto-triggers when you say:
- "技能熔炉" — Full pipeline (create → evaluate → publish)
- "技能评估" — Evaluation only (SkillHub benchmarking + Tencent 9-dimension)
- "技能发布" — Publishing only (GitHub + ClawHub)

### Two Modes

1. **Context-rich mode**: Skip interview if 4+ essential elements are already present in conversation
2. **Interview mode**: 2-5 round adaptive interview to progressively lock down requirements

### Pipeline

```
Phase 0: Intent recognition → Element check (5 items) → Adaptive interview (2-5 rounds)
Phase 1: Creation → Description-first → 4+1 module content → 6-layer validation (with security + scoring + baseline)
Phase 2: SkillHub peer benchmarking → Search & rank → Tencent 9-dimension comparison → Gap analysis
Phase 3: Publish to GitHub + ClawHub → Security audit → Push → Verify
```

## File Structure

```
skill-forge/
├── SKILL.md                              # Main entry (≤200 lines, navigation only)
├── references/
│   ├── interview-flow.md                 # Interview flow reference
│   ├── interview-methods.md              # Interview methodology
│   ├── benchmarking-guide.md             # SkillHub benchmarking guide
│   ├── publishing-guide.md               # Publishing guide
│   └── meeting-action-extractor-example.md  # Full Skill example
├── README.md                             # This file (bilingual)
├── CHANGELOG.md                          # Version changelog
├── LICENSE                               # MIT-0
└── .claude-plugin/
    └── plugin.json                       # Plugin metadata
```

### Created Skill Directory Structure

```
<skill-name>/
├── SKILL.md                  # Main entry (≤200 lines, navigation only)
├── references/               # Long docs, style guides, detailed cases, methodology
├── scripts/                  # Executable scripts (checks, exports, batch processing)
├── assets/                   # Templates, schemas, example files, output styles
├── README.md                 # Human-readable docs (bilingual)
├── CHANGELOG.md              # Version changelog
├── LICENSE                   # MIT-0
└── .claude-plugin/
    └── plugin.json           # Plugin metadata
```

## Core Methodology

### Three Iron Rules

| Rule | Description | Consequence of Violation |
|------|-------------|--------------------------|
| Description-first | AI scans all Skill descriptions every conversation; vague = never triggers = dead Skill | Auto-trigger failure |
| One-Skill-One-Job | Multi-purpose Skills trigger chaotically and output inconsistently | Unpredictable output |
| Progressive Disclosure | SKILL.md ≤200 lines (navigation only); details split into references/scripts/assets | Context bloat → quality decay |

### Security Red Lines (7 items)

Any created Skill must pass security check. Any red flag below = reject:

1. curl/wget to unknown URLs or sending data to external servers
2. Requesting credentials/tokens/API keys without clear reason
3. Reading ~/.ssh, ~/.aws, ~/.config, MEMORY.md, USER.md, IDENTITY.md
4. Using base64 decode / eval() / exec() with external input
5. Modifying system files outside workspace or requesting sudo
6. Obfuscated code (compressed, encoded, minified)
7. Accessing browser cookies/sessions or credential files

### 6-Layer Validation

| Layer | What to validate | Method |
|-------|-----------------|--------|
| 1 | Can it run? | Functional test |
| 2 | Can it trigger correctly? | 5 positive + 3 negative real user queries |
| 3 | Dogfood simulation | Format match + rule compliance + edge cases |
| 4 | Quantitative scoring | 0-10 scale, main use cases ≥5 |
| 5 | Baseline comparison | With Skill vs without Skill, verify value-add |
| 6 | Iterative fix | Fix failures → re-run validation |

## Documentation

| Document | Description |
|----------|-------------|
| [Interview Flow](references/interview-flow.md) | B1-B6 rules, round templates, recursive search pattern |
| [Interview Methods](references/interview-methods.md) | Behavioral probing, bias detection, option design |
| [Benchmarking Guide](references/benchmarking-guide.md) | SkillHub API usage, quality ranking formula, 9-dimension template |
| [Publishing Guide](references/publishing-guide.md) | Repo structure template, security audit, GitHub API fallback, ClawHub CLI |
| [Full Example](references/meeting-action-extractor-example.md) | Meeting action extractor Skill example |

## License

MIT-0 © 2026 AI花生
