# cybernetic-thinking

> **中文** | [English](README.md)

---

## 这是什么

一个给 AI 编程助手用的 skill。它做的事情很简单：在写代码之前，让模型先用控制论和系统论的视角把问题想清楚——状态是什么、能不能观测、稳不稳定、边界在哪、耦合怎么处理——然后再动手。

这个 skill 不教模型怎么写代码，而是教它怎么*想*。两本书作为底子：

- 钱学森、宋健《工程控制论》——数学基础：稳定性、反馈、多变量解耦、扰动补偿、有界控制、离散系统。
- 金观涛《控制论与科学方法论》——认识论基础：可能性空间、共轭控制、黑箱认识论、信息与控制的依存、超稳定系统、分叉与突变。

跟语言和框架无关。服务、管线、编译器、agent loop 都能套用。

## 解决什么问题

写代码时常见的痛是：改一个地方，另一个地方坏了；修了 bug，又引入新 bug；测试过了，上线还是出问题。这些多数不是粗心，而是没搞清楚系统当前到底处于什么状态、改动会让它走向哪里。

这个 skill 适用于：

- 改一段不完全理解的遗留代码
- 调试时好时坏、复现不了的问题
- 重构互相牵制的模块
- 做既要正确又要稳的改动

## 核心思想

**程序是一个动态系统，你是控制器。**

每次改动都是往系统里注入一个控制信号。你只能部分观测真实状态。bug 是不稳定或欠阻尼的轨迹。调试是状态估计。测试是反馈回路的传感器。闭环永远比开环好。

## 安装

本 skill 面向支持自定义 skill 的 AI 编程助手（Claude Code、Codex、Kilo、WorkBuddy、Trae、Cursor、Aider 等）。

> **0.4.0 改名**：包名从 `skill-systems-thinking` 改为 `skill-cybernetic-thinking`。装过旧名的用户请先删掉旧链接：`rm -rf ~/.config/kilo/skills/skill-systems-thinking`（路径按你的 agent 调整），再装新的。

### npx 安装（推荐）

```bash
npx skill-cybernetic-thinking install
```

安装程序用 `@clack/prompts` 做了一个交互式 TUI。它先扫描你机器上装了哪些 AI 编程助手，列出来，然后引导你：只装检测到的 / 自定义选择 → 选 agent → 项目级 / 全局 → 链接。

```text
$ npx skill-cybernetic-thinking install

◇ Detected agents
  Claude Code      ~/.claude
  Codex CLI        ~/.codex
  Kilo             ~/.kilo

◆ Install for detected agents only, or add more?
│ ● Detected only (claude, codex, kilo)
│ ○ Customize...
└
◆ Install location
│ ● Project (/current/dir)
│ ○ Global (~)
└
  [ok]   ~/.claude/skills/skill-cybernetic-thinking
  [ok]   ~/.codex/skills/skill-cybernetic-thinking
  [ok]   ~/.kilo/skills/skill-cybernetic-thinking

◇ Done! installed: 3, skipped: 0, failed: 0
```

选 `Customize...` 会打开一个多选菜单（空格切换选中），列出所有已知 agent。

常用参数：

```bash
# 跳过交互，直接装到检测到的 agent
npx skill-cybernetic-thinking install -y

# 指定 agent（不交互）
npx skill-cybernetic-thinking install -a claude,codex

# 装到自定义目录（适合不在列表里的 agent）
npx skill-cybernetic-thinking install --path ~/my-agent/skills

# 只装全局路径 / 只装项目路径
npx skill-cybernetic-thinking install --global
npx skill-cybernetic-thinking install --local

# 强制覆盖已有链接
npx skill-cybernetic-thinking install --force

# 查看帮助
npx skill-cybernetic-thinking install --help
```

非 TTY 环境（CI、管道）下会跳过 TUI，直接装到所有检测到的 agent 的全局目录。

### npm install（仅下载）

```bash
npm install skill-cybernetic-thinking
```

这步只把包下载到 `node_modules`，**不会**链接到任何 agent 目录。下完还是要跑一遍：

```bash
npx skill-cybernetic-thinking install
```

### GitHub / Gitee 下载

```bash
git clone https://github.com/ShrimpLeon/cybernetic-thinking.git
# 或
git clone https://gitee.com/leon0903/cybernetic-thinking.git

cp -r cybernetic-thinking <agent-skills-dir>/
```

### 各 agent 的 skill 目录

npx 安装会自动链接。手动安装时，各 agent 的目录如下：

| Agent | Skill 目录 |
|---|---|
| Claude Code | `~/.claude/skills/` 或项目 `.claude/skills/` |
| Codex CLI | `~/.codex/skills/` 或项目 `.codex/skills/` |
| Cursor | `~/.cursor/skills/` 或项目 `.cursor/skills/` |
| Gemini CLI | `~/.gemini/skills/` 或项目 `.gemini/skills/` |
| GitHub Copilot | `~/.copilot/skills/`（用户级；项目级 `.github/skills/` 也会被 CLI 读取） |
| Kilo | `~/.kilo/skills/` 或项目 `.kilo/skills/` |
| Aider | `~/.aider/skills/` 或项目 `.aider/skills/` |
| Windsurf | `~/.windsurf/skills/` 或项目 `.windsurf/skills/` |
| Zed | `~/.zed/skills/` 或项目 `.zed/skills/` |
| WorkBuddy | `~/.workbuddy/skills/` 或项目 `.workbuddy/skills/` |
| Trae | `~/.trae/skills/`（国际版）或项目 `.trae/skills/`；国内版 / **Trae Work** 用 `~/.trae-cn/skills/`（安装器两个目录都会检查） |
| Agent Skills 标准目录（`.agents`） | `~/.agents/skills/` — 用户级共享文件夹（跨 agent 标准，Trae、Kilo、Claude 等都会读取） |

不在列表里的 agent，用 `--path` 指定目录。

### 验证安装

```bash
pwsh init.ps1
# 或
powershell -ExecutionPolicy Bypass -File init.ps1
```

看到 `Verification Complete — OK` 即可。

## 用法

### 1. 什么时候加载

- 架构设计
- 调试非确定性行为
- 跨模块重构
- 任何"既要正确又要稳"的改动

### 2. 读 SKILL.md

先读 `SKILL.md`，里面有一段运行时提示，会把 13 条认知法则装进模型的思考过程。下面的工作流是自然延伸。

### 3. 动手之前，先命名

改代码之前，必须说清楚：

- `x` — 被控变量：什么必须保持正确
- `u` — 控制变量：你实际会动的那个杠杆
- 可能性空间：你在哪些结果里选？改动后缩小了哪个集合？
- 可观测性：你怎么知道 `x` 的当前值？看不见就控制不了
- 边界：每个执行器都会饱和，不接受无界循环

### 4. 七步循环

| 步骤 | 原则 | 参考文件 |
|---|---|---|
| 1 | 识别：命名 `x`、`u`、可能性空间、可观测性、边界 | `references/state-and-control.md`、`references/possibility-space.md` |
| 2 | 分析：复现、测量、定位故障、把模型当黑箱假设 | `references/modeling.md`、`references/black-box-epistemology.md` |
| 3 | 稳定：在加新功能之前先消灭发散/振荡/泄露 | `references/stability.md`、`references/system-evolution.md` |
| 4 | 综合：最小 `u`；解耦有害，协调有益；必要时用共轭控制 | `references/multivariable.md`、`references/possibility-space.md` |
| 5 | 闭环：观察实际结果，修正直到偏差有界 | `references/closed-loop-workflow.md`、`references/information-and-control.md` |
| 6 | 补偿：可测扰动用前馈；有延迟就加阻尼 | `references/disturbance.md` |
| 7 | 优化：稳定之后才谈性能调优 | `references/bounded-control.md` |

涉及采样和测试节奏的问题，参考 `references/discrete-systems.md`。

### 5. 模板

以下文件在 skill 安装目录下的 `templates/`：

- 调试时：复制 `templates/debugging-checklist.md` 到会话
- 规划改动时：用 `templates/change-proposal.md` 写控制计划

### 6. 自审计

宣布完成之前，必须通过 `evals/checks.json` 中所有 MUST 检查项。

## 13 条认知法则

1. 先命名 `x` 再命名 `u`。没名字的目标就没法调节。
2. 命名可能性空间。不能缩小不确定性的改动不是控制，是动作。
3. 先观测再猜测。综合方案之前先测量当前行为。
4. 当控制失败，先怀疑缺少信息通道，而不是缺少执行器。
5. 稳定优先于优化。扰动下发散就是失败。
6. 闭环。观察实际结果，不断修正直到偏差有界。反馈放大弱控制器。
7. 可测扰动用前馈，其余用反馈。绝不在延迟回路上提高增益。
8. 解耦有害耦合，协调有益耦合。调节关系，不只是绝对值。
9. 最小控制。移动 `x` 到目标所需的最小 `u`，不做多余的改动。
10. 收敛。修正幅度必须越来越小。如果越来越大，说明不稳定——停下来重新识别。
11. 把系统当黑箱。你的模型是假设，不是内部真相。一次只开一层。
12. 让模型可证伪。动手之前说清楚，什么观察能证明你的假设错了。
13. 识别超稳定和分叉。有些不稳定是修复机制；在分叉点上，小选择会锁定大差异。

## 工作示例

**问题**：一个 API 接口在负载下间歇性返回 500。

| 步骤 | 控制论行动 |
|---|---|
| 识别 | `x` = 错误率；`u` = 重试/超时/缓存逻辑；边界 = 请求预算。可能性空间 = {超时太短, 依赖慢, 重试风暴, 缓存击穿, ...}。改动必须缩小这个集合。 |
| 分析 | 在负载下复现；测量错误率随并发上升（不稳定）。假设：重试风暴。可证伪预测：如果重试次数限制为 2 并加退避，依赖 p99 应降到 500ms 以下。 |
| 稳定 | 加熔断器 + 带退避的有界重试 → 错误率有界。识别为振荡，不是稳态漂移。 |
| 综合 | 最小改动，不重写服务。 |
| 闭环 | 再次压测；错误率收敛到接近 0，而不是继续增长。 |
| 补偿 | 对可测依赖故障快速失败（前馈）+ 其余用反馈。 |
| 优化 | 此时才 trim p99 延迟。 |

**没有这套视角的常见失败**：无限制加重试 → 重试风暴（不稳定延迟环）→ 下一个"修复"把重试全删了（反馈过度，方向反转）→ 原 bug 回来。第 10 和第 13 条专门拦这两种错。

## 参考文件

12 篇深度参考，每篇都锚定到原著，并附 LLM 行为模式说明：

| 主题 | 文件 |
|---|---|
| 闭环工作流 | `references/closed-loop-workflow.md` |
| 状态、控制、可观测性、边界 | `references/state-and-control.md` |
| 稳定性（含稳态结构、反馈过冲、超稳定） | `references/stability.md` |
| 建模与模型有效性 | `references/modeling.md` |
| 多变量：解耦与协调 | `references/multivariable.md` |
| 扰动补偿与时延 | `references/disturbance.md` |
| 有界控制 | `references/bounded-control.md` |
| 离散系统与测试节奏 | `references/discrete-systems.md` |
| 可能性空间与共轭控制 | `references/possibility-space.md` |
| 黑箱认识论与可证伪性 | `references/black-box-epistemology.md` |
| 信息与控制的依存 | `references/information-and-control.md` |
| 系统演化：稳态、超稳定、分叉、突变 | `references/system-evolution.md` |
| 两本书的原文摘录 | `references/original-text.md` |

## 自审计

`evals/checks.json` 列了一组 MUST/SHOULD 检查项，供 LLM 或评审者确认思维 discipline 被遵循。在所有 MUST 项通过之前，不得宣布任务完成。

## 贡献

- `SKILL.md` 中的每条主张都必须追溯到某个参考文件
- 每个引用链接必须能解析到存在的文件
- 保持 skill 精简，与两本书保持一致
- 提交前运行 `./init.ps1`

完整工作规则见 `AGENTS.md`。

## 版本

本 skill 遵循 [Semantic Versioning](https://semver.org/)（`X.Y.Z`）。

| 版本 | 日期 | 说明 |
|---|---|---|
| 0.6.0 | 2026-08-09 | 扩充 agent 注册表并改为多根检测：新增 **WorkBuddy**（`~/.workbuddy`）、**Trae**（国际版 `~/.trae` + 国内版 / Trae Work `~/.trae-cn`），以及跨 agent 的 **Agent Skills 标准 / 用户级 `.agents`** 文件夹（`~/.agents/skills`）。Kilo 现在也会识别 `~/.kilocode`。自定义安装现在可以选择装到 `~/.agents/skills`。修复 **GitHub Copilot** 误检：改为指向真正的用户级目录 `~/.copilot/skills`，不再用 `~/.github`（只装了 git / GitHub Desktop / gh 的机器也会存在 `~/.github`，会误判）。 |
| 0.5.0 | 2026-08-05 | 用 `@clack/prompts` 重写 `scripts/install.js` 的 TUI 交互（检测 → 选择 → 位置 → 安装 → 完成）；修复 `install` 子命令崩溃；新增 Gemini CLI；非 TTY 自动降级。给 `SKILL.md` frontmatter 加 `author`/`tags` + `package.json` 加 `skills-sh` keyword 以支持 skills.sh 收录。 |
| 0.4.0 | 2026-07-30 | **改名**：`skill-systems-thinking` → `skill-cybernetic-thinking`（包名、仓库名、skill 名同步）。旧包在 npm 标记为 deprecated。 |
| 0.3.1 | 2026-07-30 | 删除冗余的 `assets/runtime-prompt.txt`（内容已在 `SKILL.md` 内联）；清理 `assets/` 目录及相关引用 |
| 0.3.0 | 2026-07-30 | 整合《控制论与科学方法论》；新增 4 篇参考、5 条认知法则；重写 install 交互（列表 + 选择 + 自定义路径） |
| 0.2.0 | 2026-07-26 | 安装 CLI 新增 agent 选择和位置 flags |
| 0.1.5 | 2026-07-25 | 分离 README.md / README_CN.md；统一版本号 |
| 0.1.4 | 2026-07-25 | 缺陷修复 |
| 0.1.3 | 2026-07-25 | 统一项目版本号；添加 XYZ 版本约定到 AGENTS.md；移除 postinstall 脚本 |
| 0.1.2 | 2026-07-25 | 添加 Gitee 下载链接；更新 repository 和 homepage 到 Gitee |
| 0.1.1 | 2026-07-24 | 修复 repository.url；扩展 keywords；添加 homepage 和 bin 字段 |
| 0.1.0 | 2026-07-24 | 首次公开发布 |

完整变更记录见 [CHANGELOG.md](CHANGELOG.md)。

## 协议

MIT License。详见 [LICENSE](LICENSE)。

## 来源

- 钱学森、宋健《工程控制论》（*Engineering Cybernetics*）——数学基础。
- 金观涛《控制论与科学方法论》（*Cybernetics and Scientific Methodology*）——认识论基础。

两本书的原文及数学推导是权威来源；本 skill 是基于两本书的提炼与实践化解读，不是替代。
