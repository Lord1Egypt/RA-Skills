<p align="center"><b>Language</b>: <a href="./README.md">English</a> · 中文</p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-verify-mcp banner" width="100%" />
</p>

<h1 align="center">yotta-verify-mcp · 元信MCP (YuanXin MCP)</h1>

<p align="center">YottaMeta 的 <b>装前安全扫描器</b>，做成一个 <b>stdio MCP server</b>：安装任何技能 /
插件 / MCP 服务器之前，先跑一次 <b>确定性静态扫描</b>——提示注入、危险模式、SKILL.md 完整性、
权限需求——然后通过 MCP 工具返回 <b>verdict</b>、<b>audited 徽章</b>、CI <b>闸门</b> 与
<b>报告</b>。</p>
<p align="center">触发场景：在 MCP 客户端配置元信 MCP、把装前信任扫描接入智能体 / 工作流、
调用上述 MCP 工具做扫描。</p>
<p align="center">零依赖（Python 3.8+ 标准库）；Windows + Linux + macOS；纯本地离线——
不联网、不执行被测代码。</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-verify-mcp"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-verify-mcp" /></a>
  <a href="https://github.com/YottaMeta/yotta-verify-mcp"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-verify-mcp" /></a>
  <a href="https://github.com/YottaMeta/yotta-verify-mcp/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-verify-mcp" /></a>
  <a href="https://github.com/YottaMeta/yotta-verify-mcp"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
</p>

## 这是什么

技能 / 插件市场有一个信任问题：22,511 个技能普查发现 140,963 个问题，其中 <b>36% 含提示注入</b>。
元信 MCP 在「装之前」给你一个 <b>确定性答案</b>——与 [yotta-verify](https://github.com/YottaMeta/yotta-verify)
CLI 同一套扫描，暴露成四个 MCP 工具，让任意 MCP 客户端（Claude / VS Code / Codex / Cursor 等）都能调用。

它是<b>装前验证器</b>，不是沙箱也不是运行时监控：只读文件、出报告；绝不执行被测代码、
扫描过程中不联网、绝不修复任何东西。

## 为什么用它

| 优势 | 说明 |
|---|---|
| **装前信任** | 任何技能 / MCP 服务器先给确定性 verdict，而不是「请相信我」 |
| **零依赖** | Python 3.8+ 标准库；无守护进程 / 数据库 / 联网 |
| **纯本地离线** | 扫描磁盘上的目录与 npm 包；不执行、不上传 |
| **接入任意 MCP 客户端** | 标准 stdio MCP server——配置好 server，四个工具即出现 |
| **家族协同** | 与元信 CLI 同一规则表（单源）；verdict 可与元审 / 元安合并 |
| **开源** | MIT |

## MCP 工具一览

| 工具 | 说明 |
|---|---|
| `scan_skill` | 装前扫描：`target`（目录 / .tgz / npm 包）→ verdict + 严重级统计 + 发现 |
| `generate_badge` | audited 徽章：本地 SVG + shields.io URL；并入 validate / vetter / audit / version / tests |
| `gate_check` | CI 闸门：最严重级超过 `max_severity`（默认 medium）即不过 |
| `get_report` | 验证报告：Markdown 或 JSON，与 CLI 同格式 |

## MCP 客户端配置

MCP 配置是可选项。AI 可以先展示目标配置文件、完整 `mcpServers` JSON 与影响，等你明确同意后再写入；你拒绝时不写，直接使用内置 CLI 扫描，结果一致。两种配置写法见 `SKILL.md`（本地 Python 或 npx）。

## 工具参考

### `scan_skill`

安装前扫描一个技能目录 / 包。

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `target` | string | 是 | 技能目录路径、`.tgz` / `.tar.gz` 路径，或 npm 包名（自动 `npm pack` 到临时目录后扫描） |

返回 JSON：verdict、严重级统计、发现列表（提示注入 / 危险模式 / SKILL.md 完整性）。

### `generate_badge`

生成 audited 徽章（本地 SVG + shields.io URL）。

| 参数 | 类型 | 说明 |
|---|---|---|
| `target` | string | 可选：扫描它来取得 verdict |
| `verdict` | string | 可选：直接指定 verdict |
| `validate` | string | 可选：`pass` / `fail`（validate-skill 结果） |
| `vetter` / `audit` | string | 可选：要并入的 verdict |
| `version` | string | 可选：版本标签。默认取 <b>扫描引擎（yotta-verify）版本</b>（如 0.1.1） |
| `tests` | integer | 可选：引擎测试数 |
| `out` | string | 可选：将 SVG 写入该路径 |

> 注意：徽章的 `version` 段反映的是包内 <b>扫描引擎</b>（yotta-verify）的版本，可能与 MCP 包版本不同。
> 想显示别的版本请传 `version`。

### `gate_check`

CI 装前闸门。

| 参数 | 类型 | 说明 |
|---|---|---|
| `target` | string | 必填：要扫描的目录 / 包 |
| `max_severity` | string | 可选：`info` / `low` / `medium` / `high` / `critical`（默认 `medium`） |

返回 `pass`、`verdict`、`worst`、`max_severity` 与退出码 `code`。

### `get_report`

生成验证报告。

| 参数 | 类型 | 说明 |
|---|---|---|
| `target` | string | 必填：要扫描的目录 / 包 |
| `format` | string | 可选：`json` / `markdown`（默认 `markdown`） |
| `out` | string | 可选：将报告写入该路径 |

## 边界

这是<b>本地、离线、静态</b>扫描：

- **目录扫描**完全离线——内容绝不离开你的机器。
- **npm 包扫描**只是把公开包下载到临时目录（随后删除）；不上传你的内容，也不执行被扫包代码。
- 不做动态分析、不修复任何东西、不代替你的最终决策。把 verdict 当作强信号，安装与否请自行确认。
- 只扫描你<b>有权评估</b>的目标。

## 技能安装

该包还带一份 `SKILL.md`，让智能体学会如何在用户明确同意后配置与使用这个 MCP server。以下四种方式任选
（技能文件一律从 **npm** 获取；GitHub 无代理较慢）。

### 方式一：npm 一行装（推荐）

```text
# 可选国内加速：npm config set registry https://registry.npmmirror.com
npx -y @yottameta/yotta-verify-mcp --agent <智能体名称>     # 装到指定智能体默认用户级技能目录
npx -y @yottameta/yotta-verify-mcp --dir <技能目录>        # 指到技能目录本身（如 ~/.codex/skills）
```

- `--agent <name>` 自动装到该智能体默认用户级目录；`--list` 可查看各智能体默认目录。
- `--dir <路径>` 装到指定目录。
- 不带参数运行即启动 MCP server：`npx -y @yottameta/yotta-verify-mcp`。

### 方式二：git clone（开发者 / 有 git 环境）

```text
git clone https://github.com/YottaMeta/yotta-verify-mcp.git <智能体的技能目录>/yotta-verify-mcp
```

### 方式三：GitHub 下载压缩包（手动 / 无 git 环境）

在 GitHub 仓库 `YottaMeta/yotta-verify-mcp` 点 **Code → Download ZIP**，解压后把
`yotta-verify-mcp` 文件夹放进智能体技能目录。

### 方式四：install.sh（多智能体一键脚本）

```text
bash install.sh --agent <name>   # 装到指定智能体默认用户级目录
bash install.sh --dir <path>     # 装到指定目录
bash install.sh --list           # 列出智能体 -> 默认目录
```

## 开发与校验

仓库校验包含 MCP 引擎测试与文档授权边界回归：

```bash
# MCP 引擎用例（Python 3.8 / 3.13）
python scripts/test_yotta_verify_mcp.py

# 文档授权边界回归
node --test test/docs-consent.test.js

# 直接跑 MCP server 用于调试
python scripts/yotta_verify_mcp.py
```

参考资料：`references/trust-checklist.md`（MCP 服务器 / 插件装前信任清单）。

## 许可证

MIT © YottaMeta —— 见 [LICENSE](./LICENSE)。
