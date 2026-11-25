<p align="center"><b>Language</b>: <a href="./README.md">English</a> · 中文</p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-partner banner" width="100%" />
</p>

<h1 align="center">yotta-partner · 元伴 (Yuanban)</h1>

<p align="center">YottaMeta 的 <b>人机协作提效</b> 技能：把「怎么跟 AI 把事做成」固化为一套
<b>可执行协作协议</b>——给足上下文、先方案后动手、分步交付、验证复核、交接与经验回流。</p>
<p align="center">常驻注入：每次会话开始即生效；30 秒判定决定何时走完整协议，简单问答不会被仪式化。</p>
<p align="center">自动应用于复杂/长期任务、跨会话接续、输出不可信、反复返工，或想让与 AI 的合作
更高效、更可靠。</p>
<p align="center">无运行时、无守护进程、不联网：它是一份协议 + 模板，任何智能体在任何平台上都能照做。</p>
<p align="center">它是跨智能体协作协议的<b>最低公共层</b>：任何一侧可保留更严的本地铁律，冲突时以更严者为准。</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-partner"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-partner" /></a>
  <a href="https://github.com/YottaMeta/yotta-partner"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-partner" /></a>
  <a href="https://github.com/YottaMeta/yotta-partner/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-partner" /></a>
  <a href="https://github.com/YottaMeta/yotta-partner"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
</p>

## 这是什么

很多人跟 AI 合作失败，不是 AI 不够强，而是协作方式太粗糙：不给上下文、不让先出方案、
不验证就信输出、不做跨会话记录。元伴把这种混乱反过来，交付一套**可重复执行的协作协议**：

1. **给足上下文** — 背景、目标、约束、验收标准。
2. **先方案后动手** — AI 先给方案，用户确认后才执行。
3. **分步交付** — 一个里程碑推进，每步可见、可检查。
4. **验证复核** — 逐条对验收、给可溯源证据、用户复核，不盲目相信输出。
5. **交接与回流** — 留交接锚点、存经验，让下个会话更顺。

它不是鸡汤合集，而是一套可以照抄执行的协议和模板。

### 定位

元伴是跨智能体协作协议的**最低公共层**，只规定「怎么跟 AI 把事做成」的最小公约数。
任何智能体或团队都可以保留自己更严的本地铁律（更细的状态文件规范、更严的发布闸门、
更高的证据要求）；两者冲突时，以更严者为准。

## 核心价值

| 优势 | 说明 |
|---|---|
| **常驻但轻量** | 会话开始即生效；30 秒任务判定保证简单问题不被套仪式 |
| **可执行，不是口号** | 固定协议单元：上下文模板、方案闸门、里程碑、验证、交接 |
| **跨智能体通用** | 平台中立 Markdown；无需运行时、守护进程或联网 |
| **最低公共层** | 跨智能体协作的最小公约数；更严的本地铁律始终优先 |
| **对症常见失败模式** | 不给上下文、未批准直接动手、不验证就信、跨会话全忘 |
| **可验证，不是表演** | 验收写成可勾选清单；未核实结论显式标注；证据必须是真实输出 |
| **异常自纠** | 命中常见失败信号（未批准直接动手 / 伪完成 / 状态丢失）自动停下补救，并输出一句可见提示 |
| **人的位置清晰** | 用户负责方向、判断和最终复核；AI 负责执行和记忆 |
| **越用越顺** | 踩坑和有效做法沉淀下来，供下次合作复用（可接元习） |
| **边界诚实** | 只讲协作提效；不含营销、运营与交易类话题 |

## 快速流程

```text
用户：我需要把旧报表管道迁移到新 API。
AI：  请先说明背景、目标、约束和验收标准。
用户：背景：月报依赖已下线的接口。目标：切到新 API。
      约束：不能停机，页面已有数据。验收：dry-run 通过，正式跑一次无异常。
AI：  方案：1) 盘点接口使用点，2) 写适配层，3) dry-run，4) 正式切换。
      会动的文件、验证步骤、待确认问题。可以开始吗？
用户：批准。
```

AI 若跑偏——未给方案就动手、说完成但没证据、跨会话状态丢失——会自动停下补救并输出
一句可见提示；任何时候说「按元伴检查一下」即可让它自查。

详细模板见 `references/collaboration_protocol.md`；异常与边界情形操作指引见
`references/exception_playbook.md`；完整走查示例见 `references/walkthroughs.md`；常见错误与
修复见 `references/faq.md`。

## 安装

以下四种方式任选，顺序即推荐优先级；技能文件一律从 **npm** 获取（GitHub 无代理较慢，npm 支持镜像）。

### 方式一：npm 一行装（推荐）

```text
# 可选国内加速：npm config set registry https://registry.npmmirror.com
npx -y @yottameta/yotta-partner --agent <智能体名称>      # 装到指定智能体默认用户级技能目录
npx -y @yottameta/yotta-partner --dir <智能体的技能目录>  # 指到技能目录本身（如 ~/.codex/skills）
```

- `--agent <name>` 自动装到该智能体默认用户级目录；`--list` 可查看各智能体默认目录。
- `--dir <路径>` 装到指定的技能目录；未收录的智能体用 `--dir` 指到它的技能目录。
- npmmirror 未同步新包（404）：加 `--registry=https://registry.npmjs.org/`（国内需代理），或稍等镜像缓存。

### 方式二：git clone（开发者 / 有 git 环境）

```text
git clone https://github.com/YottaMeta/yotta-partner.git <智能体的技能目录>/yotta-partner
```

### 方式三：GitHub 下载压缩包（手动 / 无 git 环境）

在 GitHub 仓库 `YottaMeta/yotta-partner` 点 **Code → Download ZIP**，解压后把 `yotta-partner`
文件夹放进智能体技能目录。

### 方式四：install.sh（多智能体一键脚本）

```text
bash install.sh --agent <name>   # 装到指定智能体默认用户级目录
bash install.sh --dir <path>     # 装到指定目录
bash install.sh --list           # 列出智能体 -> 默认目录
```

> 方式一走 npm 源（npmmirror / npmjs），不依赖 GitHub；方式二 / 三走 GitHub，国内无代理可能失败。

## 许可证

MIT © YottaMeta —— 见 [LICENSE](./LICENSE)。
