---
name: skill-polisher
description: "当用户需要持续打磨和进化技能、追踪技能质量、收集反馈改进、检查技能规范合规性时使用。每次技能执行后自动收集用户评分，沉淀使用数据，定期分析并输出改进建议。包含技能健康度检查、最佳实践沉淀、标准化评分卡等功能。🔒 只读分析，不修改任何技能文件。"
metadata:
  author: catpuru
  version: "1.0.2"
  permissions:
    reads: ["~/.openclaw/workspace/skills/"]
    writes: ["~/.openclaw/workspace/.skill-polisher/"]
    modifies_other_skills: false
---

# Skill Polisher - 技能打磨系统

让技能越用越好用的进化引擎。

## 运行模式（重要）

🔒 **只读分析**：skill-polisher 只读取技能文件进行分析，生成改进建议，**不会修改任何技能文件**。

### 功能范围

- ✅ 收集用户反馈
- ✅ 分析反馈数据，识别问题模式
- ✅ 生成健康报告
- ✅ 输出改进建议
- ❌ **不修改 SKILL.md**
- ❌ **不修改脚本代码**
- ❌ **不修改文件权限**

### 改进建议输出位置

所有改进建议输出到 `~/.openclaw/workspace/.skill-polisher/polish-history/`，用户自行决定是否采纳。

---

## 核心流程

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  技能执行    │ → │  评分收集    │ → │  数据沉淀    │ → │  输出建议    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
     只读              只读              只读              只读
```

🔒 全流程只读，不修改任何技能文件。

## 快速开始

### 1. 技能执行后自动收集反馈

每次技能执行完毕，自动询问用户：

> **任务完成度评分 (0-10)**：7  
> **主观评价**：输出格式不太对，需要调整  
> **遇到的问题**：表格渲染有问题

### 2. 查看技能健康报告

```bash
# 查看所有技能健康度
python3 scripts/health-report.py

# 查看单个技能详情
python3 scripts/health-report.py learning-analyzer

# 生成改进建议
python3 scripts/polish-suggest.py
```

### 3. 生成改进建议

```bash
# 对指定技能生成改进建议
python3 scripts/polish-suggest.py --skill learning-analyzer

# 或：根据健康报告自动选择最需要改进的技能
python3 scripts/polish-suggest.py --auto
```

建议输出到 `~/.openclaw/workspace/.skill-polisher/polish-history/<skill>/<date>-suggest.md`

## 数据存储

```
~/.openclaw/workspace/.skill-polisher/
├── feedback/                    # 用户反馈记录
│   ├── learning-analyzer/
│   │   ├── 2026-03-14-001.json
│   │   └── 2026-03-15-002.json
│   └── code-reviewer/
│       └── ...
├── expectations/               # 技能成功标准（每个技能一个）
│   ├── learning-analyzer.json
│   └── code-reviewer.json
├── metrics/                    # 聚合指标
│   ├── skill-health.json
│   └── trends.json
├── polish-history/            # 打磨历史
│   └── learning-analyzer/
│       ├── 2026-03-10-polish.md
│       └── 2026-03-15-polish.md
└── knowledge-base/
    ├── best-practices.md
    ├── pitfalls.md
    └── quality-standards.md
```

## 评分维度

简化评分，只有一个维度：

| 维度 | 说明 | 范围 |
|------|------|------|
| **综合评分** | 整体满意度 | 0-10 |

## 健康度计算

```
Skill Health Score = 
  近期平均分 × 10 × 40% + 
  使用频率 × 10 × 20% + 
  成功率 × 30% + 
  反馈丰富度 × 10 × 10%
```

**等级划分：**
- 🟢 优秀 (80-100)：保持现状，可作为标杆
- 🟡 良好 (60-79)：小有瑕疵，可轻度优化
- 🟠 需关注 (40-59)：有明显问题，建议打磨
- 🔴 需重构 (<40)：问题严重，需要大幅改进

## 打磨触发条件

自动触发：
- 健康度连续 7 天低于 60
- 单次评分低于 4 分
- 累计收到 3 条同类负面反馈

手动触发：
- 用户主动要求打磨某个技能
- 定期复盘时批量检查

## 打磨流程（只读分析）

```
1. 读取技能当前状态 (SKILL.md + scripts/)
2. 分析反馈数据，识别问题模式
3. 对比 best-practices.md 检查差距
4. 生成改进建议
5. 输出建议到 polish-history/
6. 显示建议给用户
```

**用户自行决定**是否采纳建议，手动修改技能文件。

---

## 知识沉淀

### 最佳实践 (best-practices.md)

```markdown
## 文档编写

### SKILL.md 结构
- 必须有 YAML frontmatter (name + description)
- description 要说明"什么时候用这个技能"
- Quick Start 放在最前面
- 复杂流程用 mermaid 图

### 命名规范
- 技能名：小写 + 连字符，如 `code-reviewer`
- 脚本名：动词开头，如 `review.py`, `analyze.sh`

## 脚本设计

### 错误处理
- 所有脚本必须有 `set -e` 或等价处理
- 错误信息要包含上下文（哪个文件、哪一步）

### 输出格式
- 进度信息输出到 stderr
- 结果输出到 stdout（便于管道）
- 支持 `--json` 输出模式（可选但推荐）
```

### 踩坑记录 (pitfalls.md)

```markdown
## 2026-03-14 | 技能名过长导致加载失败

**问题**：skill 名称超过 64 字符，OpenClaw 无法识别  
**解决**：限制名称长度，使用缩写  
**预防**：创建时检查名称长度

## 2026-03-10 | 脚本依赖未声明

**问题**：脚本依赖外部工具，但 SKILL.md 没说明  
**解决**：在 Quick Start 中添加依赖安装步骤  
**预防**：创建检查清单，强制检查依赖声明
```

### 质量标准 (quality-standards.md)

```markdown
## SKILL.md 必备检查项

- [ ] YAML frontmatter 完整
- [ ] description 包含使用场景
- [ ] 有 Quick Start 章节
- [ ] 所有脚本路径正确
- [ ] 示例代码可运行

## 脚本必备检查项

- [ ] 有执行权限
- [ ] 有 shebang
- [ ] 错误处理完善
- [ ] 帮助信息 (-h/--help)
- [ ] 参数校验

## 进阶标准

- [ ] 有单元测试
- [ ] 支持 CI 集成
- [ ] 有版本变更记录
```

## 集成到技能执行流程

skill-polisher 作为技能被 Agent 加载后，Agent 根据任务完成情况自主判断是否触发反馈收集。

🔒 **全流程只读**：反馈收集、健康报告、改进建议都不会修改任何技能文件。

### 触发时机

Agent 在完成技能任务后，自主判断是否需要收集反馈：

1. **任务完成且用户确认满意** → 询问评分
2. **用户主动反馈问题** → 记录问题
3. **复杂/重要任务** → 必须收集反馈

### 询问模板

```
任务已完成。

📊 请对本次执行评分 (0-10): ___
📝 遇到的问题或建议 (可选): ___
```

### Agent 调用方式

Agent 询问用户后，调用以下命令记录反馈：

```bash
# 交互式收集（询问用户）
python3 ~/.openclaw/workspace/skills/skill-polisher/scripts/collect-feedback.py \
    --skill <skill-name>

# 或命令行直接记录（已知评分时）
python3 ~/.openclaw/workspace/skills/skill-polisher/scripts/collect-feedback.py \
    --skill <skill-name> --score 8 --comment "运行很快"
```

**注意**：以上由 Agent 自主执行，不涉及修改任何技能脚本。

## Agent 使用规范

### 技能生命周期管理

**1. 管理追踪列表**

只有用户明确要求打磨的技能，才会加入追踪列表：

```bash
# 查看追踪列表
python3 ~/.openclaw/workspace/skills/skill-polisher/scripts/tracking.py

# 添加技能到追踪列表（开始打磨）
python3 ~/.openclaw/workspace/skills/skill-polisher/scripts/tracking.py --add <skill-name>

# 从追踪列表移除（停止打磨，历史数据保留）
python3 ~/.openclaw/workspace/skills/skill-polisher/scripts/tracking.py --remove <skill-name>

# 查看追踪状态
python3 ~/.openclaw/workspace/skills/skill-polisher/scripts/tracking.py --status
```

**2. 为新技能设置成功标准（可选）**

```bash
# 交互式设置成功标准
python3 ~/.openclaw/workspace/skills/skill-polisher/scripts/set-expectation.py --skill <name> --edit
```

成功标准包含：
- **核心功能**：这个技能是做什么的（一句话）
- **成功标准**：用户怎么判断任务完成了？（ checklist ）
- **常见失败**：什么情况下算没完成？
- **预期输出**：应该产生什么结果？

**3. 检查规范合规性（可选）**

```bash
# 检查技能是否符合 https://agentskills.io/specification
python3 ~/.openclaw/workspace/skills/skill-polisher/scripts/check-spec.py --skill <name>
```

**4. 执行技能后：收集反馈（仅追踪列表中的技能）**

询问模板：
```
任务已完成。

📊 请对本次执行评分 (0-10): ___
📝 遇到的问题或建议 (可选): ___
```

记录反馈：
```bash
# 交互式收集
python3 ~/.openclaw/workspace/skills/skill-polisher/scripts/collect-feedback.py --skill <name>

# 命令行直接记录
python3 ~/.openclaw/workspace/skills/skill-polisher/scripts/collect-feedback.py \
    --skill <name> --score 8 --comment "运行很快"
```

⚠️ **注意**：只有追踪列表中的技能才能收集反馈。如果技能不在列表中，会提示：
```
⚠️  <skill-name> 不在追踪列表中
   使用 tracking.py --add <skill-name> 添加到追踪列表
```

**5. 定期复盘：查看健康报告（仅追踪列表中的技能）**

```bash
# 查看所有追踪中技能的健康报告
python3 ~/.openclaw/workspace/skills/skill-polisher/scripts/health-report.py

# 查看单个技能
python3 ~/.openclaw/workspace/skills/skill-polisher/scripts/health-report.py <name>
```

**6. 持续改进**

```bash
# 生成改进建议
python3 ~/.openclaw/workspace/skills/skill-polisher/scripts/polish-suggest.py --skill <name>

# 查看建议
cat ~/.openclaw/workspace/.skill-polisher/polish-history/<name>/<date>-suggest.md
```

🔒 **只读**：建议输出到文件，用户自行决定是否采纳。

## 成功标准示例

### learning-analyzer

```json
{
  "purpose": "自动分析学习历程数据，生成知识点掌握度报告",
  "success_criteria": [
    "正确识别所有输入文件格式",
    "输出包含知识点掌握度统计",
    "生成可视化图表或清晰的数据表格",
    "报告格式整洁、易于阅读"
  ],
  "failure_modes": [
    "文件解析失败或格式错误",
    "输出数据不完整或明显错误",
    "缺少关键统计指标",
    "报告格式混乱难以阅读"
  ],
  "expected_output": "Markdown 格式的分析报告，包含数据表格"
}
```

### code-reviewer

```json
{
  "purpose": "系统化审查代码，发现潜在问题和改进点",
  "success_criteria": [
    "覆盖所有关键检查项（安全、性能、可维护性）",
    "发现的问题有具体位置和修复建议",
    "生成结构化的审查报告",
    "评分合理，有改进优先级"
  ],
  "failure_modes": [
    "遗漏明显的问题",
    "误报过多（false positive）",
    "报告格式混乱",
    "没有可执行的改进建议"
  ]
}
```

## 隐私与数据安全

### 核心原则

**用户数据与技能代码绝对分离**

所有用户个人数据存储在 workspace 下的独立目录：
```
~/.openclaw/workspace/.skill-polisher/     ← 用户数据（隐私，不同步到 clawhub）
├── feedback/           # 用户评分记录
├── expectations/       # 技能成功标准
├── metrics/            # 聚合统计
└── polish-history/     # 打磨历史
```

技能代码存储在：
```
~/.openclaw/workspace/skills/skill-polisher/  ← 技能代码（可同步到 clawhub）
├── SKILL.md
├── scripts/
└── references/
```

### 为什么重要

1. **隐私保护**：用户反馈、项目信息不会泄露到公共仓库
2. **技能可共享**：技能目录可以安全地发布到 clawhub
3. **多用户安全**：不同用户的数据互不干扰

### 设计原则（所有技能必须遵守）

- ✅ 用户数据 → `~/.openclaw/workspace/.skill-name/`
- ✅ 技能代码 → `~/.openclaw/workspace/skills/skill-name/`
- ❌ 绝不在技能目录内存储用户隐私数据
- ❌ 绝不在技能目录内存储项目特定信息

## 参考文档

- [references/QUALITY-STANDARDS.md](references/QUALITY-STANDARDS.md) - 技能质量检查清单
- [references/BEST-PRACTICES.md](references/BEST-PRACTICES.md) - 最佳实践
- [references/PITFALLS.md](references/PITFALLS.md) - 踩坑记录
- [references/QUALITY-CHECKLIST.md](references/QUALITY-CHECKLIST.md) - 技能质量检查清单
- [references/DATA-SCHEMA.md](references/DATA-SCHEMA.md) - 数据格式规范

## TODO

- [ ] 创建数据存储目录结构
- [ ] 实现 collect-feedback.py 评分收集
- [ ] 实现 health-report.py 健康报告
- [ ] 实现 polish-suggest.py 改进建议（只读）
- [ ] 填充 best-practices.md 初始内容
- [ ] 填充 pitfalls.md 初始内容（基于已有技能经验）
- [ ] 创建 QUALITY-CHECKLIST.md
