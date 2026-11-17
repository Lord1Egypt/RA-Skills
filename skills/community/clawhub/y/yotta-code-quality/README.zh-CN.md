<p align="center"><b>Language</b>: <a href="./README.md">English</a> · 中文</p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-code-quality banner" width="100%" />
</p>

<h1 align="center">yotta-code-quality · 元质</h1>

<p align="center">面向 **Cursor / Codex / Claude Code / 通用 Agent** 的结对代码审查技能。把「代码质量审查」沉淀为可复用、可配置、有方法论支撑的技能，让智能体在交付前像资深工程师一样通读代码、定位劣化，并给出带依据的修复方案。</p>

<p align="center">
  一句话定位：**先诊断、再修复，只出报告不动代码。**
</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-code-quality"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-code-quality" /></a>
  <a href="https://github.com/YottaMeta/yotta-code-quality"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-code-quality" /></a>
  <a href="https://github.com/YottaMeta/yotta-code-quality/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-code-quality" /></a>
  <a href="https://github.com/YottaMeta/yotta-code-quality"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
</p>

## 核心价值

- **有依据，不拍脑袋。** 方法论蒸馏自 12 本经典软件工程著作（Fowler《重构》、McConnell《代码大全》、Ousterhout《软件设计哲学》、Evans《领域驱动设计》等），每条发现都锚定到具体书籍原则或坏味道。
- **铁律（Iron Law）防灌水。** 每条发现必须走 `症状 → 根源 → 后果 → 修复`（Symptom → Source → Consequence → Remedy），缺「后果」或「修复」的发现一律视为噪声，不会报出来。
- **默认只读、先诊断后修复。** 只出审查报告，不动代码；除非你明确要求 `--fix`（按 Remedy 修）。
- **健康分（Health Score）可追踪。** 每次审查给出 0–100 扣分指数（刻意定义成**单次扣分指数**，而非绝对评级），支持跨次趋势比较。
- **按需加载，不臃肿。** 按模式（Quick / PR / 架构 / 测试 / 发布）只读需要的参考文件，避免把整套方法论塞进上下文。
- **跨智能体 + 零依赖。** 纯文件技能，Cursor / Codex / Claude Code / 通用 Agent 均可用；不引入任何运行时依赖。

## 核心优势

| 维度 | yotta-code-quality | 说明 |
|------|--------------------|------|
| 方法论 | 12 本经典 SE 著作 + 坏味道 | 每条发现可溯源，非经验主义空谈 |
| 发现结构 | Iron Law 四段式 | 强制带「后果 + 修复」，避免无效吐槽 |
| 评分 | 单次扣分指数（0–100） | 明确"非绝对评级"，防误读、支持趋势 |
| 覆盖面 | R1–R6 + T1–T6 + R7 + UX1 | 生产、测试、发布/供应链、首屏体验全覆盖 |
| 配置 | `.code-quality.yaml` | 按风险开关/降级/忽略/聚焦，自适应项目 |
| 触发 | 对话即触发 | 「结对评审」「发版前扫一眼」也能命中 |
| 附加件 | AGENTS-template / hooks.json | 可选，不装不影响审查核心 |

## 工作流程（协议详解）

### 铁律（不可协商）

```
NEVER suggest fixes before completing risk diagnosis.
EVERY finding must follow: Symptom → Source → Consequence → Remedy.
Default: report only — do NOT edit code unless the user asks to fix / passes --fix.
```

### 会话契约

1. **默认只读**：只出报告，不做顺手重构。
2. **范围纪律**：用户点名文件 / diff /「刀子」，就留在该范围内。
3. **健康分不是评级**：它是**单次扣分指数**，不是对代码库的客观打分。
4. **语言**：报告用用户语言；Iron Law 字段名、书名、坏味道名、固定表头（`Findings` / `Summary` / `Critical` / `Warning` / `Suggestion`）保留英文。

### 按需加载（Mode 路由）

| 模式 | 何时使用 | 先读 | 需要时再读 |
|------|----------|------|-----------|
| **Quick** | 粘贴函数 / &lt; 50 行 diff / 扫一眼 | `SKILL.md` + 速查 | `decay-risks.md` |
| **PR 审查** | PR / 分支 diff / ready to merge | `common.md` + `pr-review-guide.md` | `decay-risks.md` / `test-decay-risks.md` / `examples.md` |
| **架构 / 技术债** | 整模块 / 审计 / `--full` | `common.md` + `decay-risks.md` + `source-coverage.md` | `editorial-extensions.md` |
| **测试质量** | 测试 / 覆盖率 / flaky | `common.md` + `test-decay-risks.md` | `examples.md` |
| **发布 / 上架** | 发版前 / updater / CSP / 密钥 | `common.md` + `editorial-extensions.md` | R1–R6 表 |

### 评分（Health Score）

基础 100 分，按 `strictness` 扣分，下限 0。**仍会报告每一条发现**，评分只是趋势参考。

| 预设 | Critical | Warning | Suggestion |
|------|----------|---------|------------|
| `strict` | −20 | −8 | −2 |
| `balanced`（默认） | −15 | −5 | −1 |
| `legacy-friendly` | −8 | −3 | −1 |

### 配置（`.code-quality.yaml`）

审查前会在仓库根尝试读取该文件，缺失则用默认值（全部风险开启，`balanced`）。

| 字段 | 作用 |
|------|------|
| `disable` | 跳过指定风险（R1–R7 / T1–T6 / UX1） |
| `severity` | 强制某风险为 critical / warning / suggestion |
| `ignore` | 按 glob 排除（如 `**/*.generated.*`） |
| `focus` | 只审这些风险（不能与 `disable` 同时用） |
| `strictness` | strict / balanced（默认）/ legacy-friendly |
| `suppress` | 由 `--triage` 写入的忽略项 `{ id, reason, expires? }` |
| `history` | `true` 写入 `.code-quality-history.json` 趋势记录；默认关（见 History Tracking） |

```yaml
version: 1
strictness: balanced
disable: []
severity: {}
ignore:
  - "**/*.generated.*"
  - "**/node_modules/**"
suppress: []
history: false
```

### 可选参数

- `--fix` / 「按 Remedy 修」→ 进入修复模式（按 Remedy 最小改动，并重审这些发现）
- `--triage` / 「逐条处理」→ 交互式忽略 / 延期（写入 `suppress`）
- `.code-quality.yaml` 设 `history: true` → 生成 `.code-quality-history.json` 趋势记录

> 附加件 `AGENTS-template.md` 与 `hooks.json` 不装也不影响审查。

## 风险矩阵（canonical）

| 代码 | 名称 | 诊断要点 |
|------|------|----------|
| R1 | 认知过载 Cognitive Overload | 读这段代码需要多少脑力 |
| R2 | 变更传播 Change Propagation | 改一处会连带坏多少无关处 |
| R3 | 知识重复 Knowledge Duplication | 同一决策是否散落多处 |
| R4 | 意外复杂度 Accidental Complexity | 是否比问题本身更复杂 |
| R5 | 依赖失序 Dependency Disorder | 依赖方向是否一致 |
| R6 | 领域模型失真 Domain Model Distortion | 是否忠实于领域语言 |
| T1 | 测试晦涩 Test Obscurity | 是否清楚在验证什么 |
| T2 | 测试脆弱 Test Brittleness | 是否被行为等价的重构打破 |
| T3 | 测试重复 Test Duplication | 同一场景是否无层价值地重复 |
| T4 | Mock 滥用 Mock Abuse | 测试是否比行为更复杂 |
| T5 | 覆盖幻觉 Coverage Illusion | 套件是否真保护了会出错的点 |
| T6 | 架构失配 Architecture Mismatch | 套件形状是否匹配风险画像 |
| R7 | 发布 / 供应链安全 | 明文密钥、跳过校验的 updater、产物开 DevTools |
| UX1 | 首屏 / 状态清晰度 | 空窗、splash 不居中、状态文案与门禁不符 |

> 详细症状、书源、严重度与「不误报清单」见 `references/decay-risks.md`、`references/test-decay-risks.md`、`references/editorial-extensions.md`。`anti-over-flag` 在报 R1 等前先抑制噪声告警，避免「狼来了」式疲劳。

## 目录结构

```
yotta-code-quality/
├── SKILL.md                  # 入口 + 按模式按需加载的路由
├── references/
│   ├── common.md             # 配置 / 模板 / 评分（单一信息源）
│   ├── decay-risks.md        # R1–R6 生产风险
│   ├── test-decay-risks.md   # T1–T6 测试风险
│   ├── editorial-extensions.md # R7 / UX1 / 防过度告警
│   ├── source-coverage.md    # 书籍矩阵（深度模式）
│   ├── pr-review-guide.md    # 7 步 PR 审查
│   ├── examples.md           # 语气 / 评分校准
│   ├── AGENTS-template.md    # 可选：丢进仓库当 AGENTS.md 强制规范
│   └── hooks.json            # 可选：PreToolUse 拦截 rm -rf / git push --force
├── bin/install.js            # npx 跨平台安装器
├── install.sh                # 一键安装到 17 类智能体（含国内 Trae/Qwen/Comate/CodeBuddy/Kimi）
├── assets/banner.png         # 品牌头图
└── LICENSE                   # MIT
```

## 安装

以下四种方式任选，顺序即推荐优先级；技能文件一律从 **npm** 获取（GitHub 无代理较慢，npm 支持镜像）。

### 方式一：npm 一行装（推荐）

```text
# 可选国内加速：npm config set registry https://registry.npmmirror.com
npx -y @yottameta/yotta-code-quality --agent <智能体名称>      # 装到指定智能体默认用户级技能目录
npx -y @yottameta/yotta-code-quality --dir <智能体的技能目录>  # 指到技能目录本身（如 ~/.codex/skills）
```

- `--agent <name>` 自动装到该智能体默认用户级目录；`--list` 可查看各智能体默认目录。
- `--dir <路径>` 装到指定的技能目录；未收录的智能体用 `--dir` 指到它的技能目录。
- npmmirror 未同步新包（404）：加 `--registry=https://registry.npmjs.org/`（国内需代理），或稍等镜像缓存。

### 方式二：git clone（开发者 / 有 git 环境）

```text
git clone https://github.com/YottaMeta/yotta-code-quality.git <智能体的技能目录>/yotta-code-quality
```

### 方式三：GitHub 下载压缩包（手动 / 无 git 环境）

在 GitHub 仓库 `YottaMeta/yotta-code-quality` 点 **Code → Download ZIP**，解压后把 `yotta-code-quality` 文件夹放进智能体技能目录。

### 方式四：install.sh（多智能体一键脚本）

```text
bash install.sh --agent <name>   # 装到指定智能体默认用户级目录
bash install.sh --dir <path>     # 装到指定目录
bash install.sh --list           # 列出智能体 -> 默认目录
```

> 方式一走 npm 源（npmmirror / npmjs），不依赖 GitHub；方式二 / 三走 GitHub，国内无代理可能失败。
## 使用

对话中说「review this PR」「结对评审」「发版前扫一眼」，或直接调用 `/yotta-code-quality`。可选参数见上文「可选参数」。

### 示例：Quick 审查（粘贴一段函数）

```
用户：帮我看看这段函数有没有问题 / 结对评审
智能体：按 Quick 模式 → 读 SKILL + 速查 → 输出 Findings + Health Score
```

### 示例：PR 审查（带 7 步流程）

```
用户：review this PR / ready to merge?
智能体：按 PR 模式 → .code-quality.yaml 配置 → 自动 scope → 走 pr-review-guide.md 7 步
       → 输出 Findings（Critical/Warning/Suggestion 排序）+ 修复顺序建议
```

### 示例：接入项目并配置

```bash
# 1. 在仓库根放一个 .code-quality.yaml（可选）
# 2. 对话触发审查，或用 --dir 把技能装到目标智能体
```

## 升级与卸载

- **升级**：重新安装最新版覆盖即可——重跑你用的安装命令（如 `npx -y @yottameta/yotta-code-quality --agent <name>` 或 `bash install.sh --agent <name>`）。技能目录内旧文件会被替换；不影响项目中其他文件。
- **卸载**：删除目标智能体 skills 目录下的 `yotta-code-quality/` 文件夹即可。
- **无副作用**：技能不写项目外文件；可选的历史/趋势文件（`.code-quality-history.json`）只在你开启 `history: true` 时生成，位于仓库根。

## 常见问题（FAQ）

- **它和通用 code review 或 linter 有何区别？** 通用工具多基于规则/风格；本技能提供「方法论依据 + 铁律四段式 + 单次扣分指数」，聚焦系统性劣化（复杂度、传播、重复、依赖、领域建模、测试与发布安全），而非风格挑刺。
- **健康分会算出一个"分数"来判断代码好坏吗？** 不会。它是**单次扣分指数**，且明确非绝对评级，用于横向比较趋势。
- **会直接改我的代码吗？** 默认只出报告；只有你要求 `--fix` 或「按 Remedy 修」才会改，且按最小行为等价方式修改。
- **想只审某几类风险怎么办？** 用 `.code-quality.yaml` 的 `disable` / `focus` / `severity` 即可。
- **`.agents/skills` 是通用目录吗？** 不是。Claude Code 与 Codex 默认不读它；不确定时用 `--dir` 指定目标目录。
- **需要联网或装依赖吗？** 不需要。技能是零依赖的纯文件，运行只依赖宿主智能体的读文件能力。

## 来源与许可

- **方法论**蒸馏自 12 本经典软件工程著作及开源社区质量审查实践（MIT）；原始方法论版权归 hyhmrright，本技能在其基础上重写为单一自包含、跨智能体通用的版本，并增补 R7 / UX1 / 按需加载会话契约。
- **许可：** MIT —— 详见 `LICENSE`（版权人：hyhmrright（原始方法论）+ YottaMeta（本打包））。

## 参考文档

- references/faq.md
- references/walkthroughs.md
