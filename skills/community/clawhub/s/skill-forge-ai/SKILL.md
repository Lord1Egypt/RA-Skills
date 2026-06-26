---
name: "skill-forge"
description: "技能熔炉 — 锻造/评估/发布 Skill。说 技能熔炉 走全流程；说 技能评估/skill评估/评估技能 只做同类比对+腾讯9维度；说 技能发布/发布技能 只做GitHub+ClawHub推送。Do NOT use for editing existing skills, skill security vetting, or general coding tasks."
---

# 技能熔炉 v4.0

锻造 → 评估 → 发布，三入口全流程交付可自动触发、稳定输出的 Skill。

## 入口检测

**根据用户触发词，决定从哪个阶段开始：**

| 触发词 | 入口 | 执行流程 |
|--------|------|---------|
| 技能熔炉 | Phase 0 | Phase 0→1→2→3 全流程 |
| 技能评估 / skill评估 / 评估技能 | Phase 2 | 只做 SkillHub 同类比对 + 腾讯9维度 |
| 技能发布 / 发布技能 | Phase 3 | 只做 GitHub + ClawHub 推送 |

**检测到触发词后，立即跳转到对应 Phase，不执行前面的阶段。**

## 三条铁律

违反任何一条 = 废技能。

**铁律1：Description先行** — AI每轮对话扫描所有Skill的description，模糊=永远不触发=死Skill。

**铁律2：一Skill一职** — 不要把多个场景塞进一个Skill，多功能Skill触发混乱、输出不一致。

**铁律3：渐进式披露** — SKILL.md ≤200行，只放导航信息（触发/原则/步骤/验证）。详细内容按三级拆分：
- `references/` — 长文档、风格参考、详细案例
- `scripts/` — 可执行脚本（确定性操作用脚本比让模型现场生成更稳定）
- `assets/` — 模板、schema、示例文件、输出样式

## SKILL.md 格式

```markdown
---
name: "<skill-name>"
description: "<做什么 + 何时触发。核心关键词放前200字符>"
allowed-tools: "<工具白名单，如：Bash(python:*) WebFetch>"
model: "<推荐模型，如：claude-opus-4-5>"
effort: "<思考深度：low/medium/high>"
metadata:
  author: "<作者>"
  version: "<版本>"
  category: "<分类>"
---

# <技能标题>

## 任务
<一句话：只做X，不做Y和Z>

## 输出格式
<固定输出结构。每个字段格式必须具体，绝不写"整理清晰">

## 规则
<3-5条硬规则。每条必须通过实习生测试——实习生能直接执行>

## 示例
<一组完整的输入输出，覆盖边界情况>

## 故障排除（可选）
<常见错误 + 原因 + 解决方案>
```

## 必填字段

| 字段 | 位置 | 必填 | 说明 |
|------|------|------|------|
| `name` | frontmatter | **是** | kebab-case，唯一标识 |
| `description` | frontmatter | **是** | (1)做什么 + (2)何时触发 + (3)Do NOT范围。200字符以内。关键词前置。 |
| `allowed-tools` | frontmatter | 推荐 | 工具白名单。足够但不过度。 |
| `model` | frontmatter | 可选 | 推荐模型。简单任务用Haiku省钱，复杂决策用Opus换准确率。 |
| `effort` | frontmatter | 可选 | 思考深度控制。low省钱省时，high换准确率。 |
| `metadata` | frontmatter | 推荐 | author / version / category 等。 |

## 目录结构

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

---

## Phase 0: 意图识别与自适应访谈

**【入口：技能熔炉】** — 读取 [`references/interview-flow.md`](references/interview-flow.md) 获取完整访谈方法论。

### Step 0.1: 要素检查

扫描上下文中的5个关键要素：**单一场景 / 触发条件 / 输出格式 / 范围边界 / 硬约束**。

- **≥4个齐备** → 与用户确认，跳到 Phase 1
- **<4个齐备** → 进入自适应访谈（Step 0.2）

### Step 0.2: 自适应访谈（2-5轮）

每轮用选项优先问题（AskUserQuestion，3个强选项+Other）+行为追问。每轮后更新要素清单，**≥4个明确 → 进入 Phase 1**。最多5轮。

---

## Phase 1: 创建

**【入口：技能熔炉】**

### Step 1: Description先行

**格式**: `"<做什么>. 当用户说<具体触发词>时触发. Do NOT use for <排除范围>."`

**截断机制**: 核心触发关键词必须在前200字符内。尾部在~250字符处截断。

### Step 2: 撰写4+1模块内容

**任务**: 锁定边界。声明"做X"和"不做Y"。
**输出格式**: 固定输出结构。每个字段必须有具体格式，绝不写模糊指令。
**规则**: 仅3-5条。必须通过**实习生测试**。删除废话规则。
**示例**: 一组完整的输入输出。一个好示例 > 10条抽象规则。
**故障排除**（可选）: 常见错误 + 原因 + 解决方案。让Agent遇到问题时能自修复。

### Step 3: 创建目录和文件

按目录结构创建。判断是否需要 `scripts/` 和 `assets/`：
- 有确定性操作（检查、导出、批量处理）→ 创建 `scripts/`
- 有模板、样式、示例文件 → 创建 `assets/`

### Step 4: 自测验证流水线

**Step 4a: Schema检查** — name+description ✅ | <200字符 ✅ | 关键词前置 ✅ | Do NOT ✅ | 4模块 ✅ | 实习生测试 ✅ | ≤200行 ✅ | 示例含边界 ✅

**Step 4a+1: 安全红线检查** — 发现以下 RED FLAG 立即拒绝：
1. curl/wget 向未知URL发送数据
2. 无正当理由请求凭证/Token/API密钥
3. 读取 ~/.ssh、~/.aws、~/.config、MEMORY.md、USER.md、IDENTITY.md
4. 使用 base64解码/eval()/exec() 处理外部输入
5. 修改工作区外的系统文件或请求sudo权限
6. 包含混淆代码
7. 访问浏览器Cookie/会话或凭证文件

**Step 4b: 触发测试** — 准备5条真实用户说法（含口语化、改写、模糊表达），3条不应触发的反向测试。每条标记 should_trigger: true/false。

**Step 4c: Dogfood模拟** — 格式匹配 ✅ | 规则合规 ✅ | 边界情况 ✅

**Step 4d: 量化评分** — 对Dogfood结果按0-10打分：
- 0-2: 完全没完成任务
- 3-4: 勉强相关，漏掉关键要求
- 5-6: 基本可用，有明显问题
- 7-8: 质量稳定，少量细节可改
- 9-10: 非常符合预期

**Step 4e: 基线对比** — 同一任务，不用Skill跑一次 vs 用Skill跑一次。如果无Skill已7分，有Skill仍7分，说明Skill无增益。

**最多3次迭代。3次后建议"先发布V1再迭代"。**

---

## Phase 2: SkillHub 同类比对 + 腾讯9维度评估

**【入口：技能评估 / skill评估 / 评估技能】** — 读取 [`references/benchmarking-guide.md`](references/benchmarking-guide.md) 获取完整比对方法论。

### Step 5a: 搜索与排名

调用 SkillHub API: `https://api.skillhub.cn/api/v1/search?q=<keywords>`。按 `downloads × 0.4 + installs × 0.3 + stars × 0.3` 排名。取 Top 3。

### Step 5b: 腾讯手册9维度合规比对

与 Top 3 同类按9维度比对：Description触发精准度 / 关键词前置 / Do NOT范围 / 单一职责 / 4模块结构 / 输出格式具体性 / 实习生测试规则 / 示例边界覆盖 / 体积控制。

### Step 5c: 差异化与盲区分析

- 重复 → 建议安装已有Skill
- 有差异 → 明确记录差异化
- 有盲区 → 列出并附腾讯手册依据

### Step 5d: 用户决策

展示结果。用户选择：采纳修复 / 保持原样 / 安装已有。**用户决策为最终决策。**

---

## Phase 3: 发布到 GitHub + ClawHub

**【入口：技能发布 / 发布技能】** — 读取 [`references/publishing-guide.md`](references/publishing-guide.md) 获取完整发布流程。

### Step 6: 仓库结构生成

生成标准目录结构：SKILL.md / README.md(中英双语) / CHANGELOG.md / LICENSE(MIT-0) / .gitignore / .claude-plugin/plugin.json。

确认作者名、GitHub owner、版本号、ClawHub slug。

### Step 7: 发布前安全审查

三类扫描，全部 PASS 才能继续：

| 扫描项 | Grep 正则 | PASS 标准 |
|--------|----------|----------|
| 凭证泄露 | `token\|api_key\|secret\|password\|ghp_\|clh_\|sk-\|AKIA` | 仅概念提及 |
| 本地路径 | `C:\\\|D:\\\|Administrator\|\.trae-cn` | 零匹配 |
| 危险命令 | `curl\|wget\|eval\|exec\|base64\|sudo\|\.ssh` | 仅安全文档提及 |

分发物三维判定 + ClawHub slug 检查（`clawhub inspect <slug>`）。

### Step 8: GitHub 推送

优先 git push，失败时降级为 GitHub REST API 逐文件上传。创建 Release 承载详细变更说明。

### Step 9: ClawHub 发布

```bash
clawhub publish <path> --slug <slug> --version <version> --tags "<ASCII-only>" --changelog "<text>"
```

**注意**：--tags 只能用 ASCII 字符（中文会报错）。--version 必填。

### Step 10: 发布后验证

1. 检查 GitHub 仓库文件列表，确认无多余文件
2. `clawhub inspect <slug>` 确认发布成功
3. 汇报发布结果

---

## References

- **[`references/interview-flow.md`](references/interview-flow.md)** — Phase 0 访谈方法论。B1-B6 规则、轮次模板、递归搜索、收敛检查。
- **[`references/interview-methods.md`](references/interview-methods.md)** — 访谈方法论深度参考。行为追问、偏误检测、选项法设计。
- **[`references/benchmarking-guide.md`](references/benchmarking-guide.md)** — Phase 2 比对方法论。SkillHub API、质量排序公式、腾讯9维度模板。
- **[`references/publishing-guide.md`](references/publishing-guide.md)** — Phase 3 发布流程。仓库结构模板、安全审查、GitHub API降级、ClawHub CLI、PowerShell兼容。
- **[`references/meeting-action-extractor-example.md`](references/meeting-action-extractor-example.md)** — 完整Skill示例。
