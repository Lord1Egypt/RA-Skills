<p align="center"><b>Language</b>: <a href="./README.md">English</a> · 中文</p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-verify banner" width="100%" />
</p>

<h1 align="center">yotta-verify · 元信 (YuanXin)</h1>

<p align="center">YottaMeta 的 <b>装前安全验证器</b>：安装任何技能 / npm 包之前，先做一次
<b>确定性静态扫描</b>——提示注入、危险模式、SKILL.md 完整性、权限需求——然后给出一句话
<b>verdict</b> 与可随包发布的 <b>audited 徽章</b>。</p>
<p align="center">触发场景：安装 / 评估任何技能或 npm 包前、给自己的技能生成 audited 徽章、
在 CI 里加装前扫描闸门。</p>
<p align="center">零依赖（Python 3.8+ 标准库）；Windows + Linux + macOS；纯本地离线——
不联网、不执行被测代码。</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-verify"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-verify" /></a>
  <a href="https://github.com/YottaMeta/yotta-verify"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-verify" /></a>
  <a href="https://github.com/YottaMeta/yotta-verify/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-verify" /></a>
  <a href="https://github.com/YottaMeta/yotta-verify"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
</p>

## 这是什么

技能市场有一个信任问题：22,511 个技能普查发现 140,963 个问题，其中 **36% 含提示注入**。
元信在「装之前」给你一个**确定性答案**：本地扫描技能目录 / npm 包，报告发现了什么、严重到什么程度、
能不能装。

它是**装前验证器**，不是沙箱也不是运行时监控：只读文件、出报告；绝不执行被测代码、
绝不联网、绝不修复任何东西。

## 核心价值

- **确定性静态扫描**——8 检测点威胁捕获模型（供应链 / 命令执行 / 网络请求与数据外传 / 文件操作与敏感路径访问 / 提示注入 / 远程脚本拉取后即运行 / 编码混淆 / 其他）+ 提示注入 + 危险模式（61 条，含路径穿越 / MCP 工具面）+ SKILL.md 完整性 + 权限需求。
- **MCP 工具面分析（L3，新增）**——识别 MCP server 工具集，追踪「工具参数 → 危险 sink」（spawnSync / execSync / 任意文件读写）；恶意 MCP 判 **DO NOT INSTALL**。
- **双视角综合报告（新增）**——安全健康度评分（0-100）+ 8 检测点逐类 verdict + 13 行为项 + 逐文件 verdict + 修复建议指南 + 内容 hash。
- **提示注入检测**——8 类 28 条规则（指令覆盖 / 角色伪造 / 编码指令 / 数据外传 / 分隔符逃逸 /
  工具自执行 / 隐藏意图 / 凭据采集）+ base64 编码指令启发式。
- **危险模式规则与元安共用**——54 条规则与 yotta-security-audit 保持同步
  （下载即执行 / 混淆 / 持久化 / 外传 / 凭据窃取 / 网络调用 / 权限提升 / 社会工程）。
- **一句话 verdict**——SAFE TO INSTALL / REVIEW REQUIRED / INSTALL WITH CAUTION / DO NOT INSTALL，
  退出码与元安 / 元审一致。
- **audited 徽章**——本地 SVG + shields.io URL；合并 validate-skill 结果、元安 / 元审 verdict、
  版本与引擎测试数。
- **CI 闸门**——最严重级超过阈值即让流水线失败。
- **安装器 hook 声明**——通过 `before_install` manifest 让元阁在替换已装技能前执行阻断门禁，并保留本地审计证据。

## 为什么用它

| 优势 | 说明 |
|---|---|
| **装前信任** | 任何技能先给确定性 verdict，而不是「请相信我」 |
| **零依赖** | Python 3.8+ 标准库；无守护进程 / 数据库 / 联网 |
| **纯本地离线** | 扫描磁盘上的目录与 npm 包；不执行、不上传 |
| **通吃任何技能** | Agent 技能、npm 包、下载的 ZIP——指个文件夹就行 |
| **家族协同** | 危险模式规则与元安同步；verdict 可与元审 / 元安合并 |

## 命令一览

| 命令 | 说明 |
|---|---|
| scan | 装前扫描（注入 + 危险模式 + SKILL 完整性 + 权限） |
| scan --json | 结构化扫描结果 |
| scan --report report.md | 写 SKILL VERIFY REPORT（Markdown） |
| scan --badge | 扫描同时生成 audited 徽章 |
| badge | 生成 audited 徽章（本地 SVG + shields.io URL） |
| report | 生成验证报告（Markdown / JSON） |
| gate | CI 装前闸门（默认阈值 medium） |
| --version | 显示版本 |

## 使用示例

Windows 用 python，Linux/macOS 用 python3。

```bash
# 装前扫描一个技能目录
python3 scripts/yotta_verify.py scan ./some-skill

# JSON + Markdown 报告 + audited 徽章
python3 scripts/yotta_verify.py scan ./some-skill --json --report report.md --badge

# 合并验证结果的 audited 徽章
python3 scripts/yotta_verify.py badge ./some-skill --validate-skill pass     --vetter-verdict "SAFE TO INSTALL" --audit-verdict "SAFE TO INSTALL" --tests 52

# CI 闸门：最严重级超过 medium 即失败
python3 scripts/yotta_verify.py gate ./some-skill --max-severity medium
```

退出码：**0** = SAFE TO INSTALL；**1** = REVIEW REQUIRED；**2** = INSTALL WITH CAUTION；
**3** = DO NOT INSTALL；**4** = 用法 / 读取错误。

示例输出：

```
元信 yotta-verify v0.2.1 —— 装前安全扫描
目标：./some-skill（扫描 14 个文件）

verdict: SAFE TO INSTALL
发现：critical 0 / high 0 / medium 0 / low 2 / info 1
```

## 安装

以下四种方式任选，顺序即推荐优先级；技能文件一律从 **npm** 获取（GitHub 无代理较慢，npm 支持镜像）。

### 方式一：npm 一行装（推荐）

```text
# 可选国内加速：npm config set registry https://registry.npmmirror.com
npx -y @yottameta/yotta-verify@0.3.6 --agent <智能体名称>      # 装到指定智能体默认用户级技能目录
npx -y @yottameta/yotta-verify@0.3.6 --dir <智能体的技能目录>  # 指到技能目录本身（如 ~/.codex/skills）
```

- `--agent <name>` 自动装到该智能体默认用户级目录；`--list` 可查看各智能体默认目录。
- `--dir <路径>` 装到指定的技能目录；未收录的智能体用 `--dir` 指到它的技能目录。
- npmmirror 未同步新包（404）：加 `--registry=https://registry.npmjs.org/`（国内需代理），或稍等镜像缓存。

### 方式二：git clone（开发者 / 有 git 环境）

```text
git clone https://github.com/YottaMeta/yotta-verify.git <智能体的技能目录>/yotta-verify
```

### 方式三：GitHub 下载压缩包（手动 / 无 git 环境）

在 GitHub 仓库 `YottaMeta/yotta-verify` 点 **Code → Download ZIP**，解压后把 `yotta-verify` 文件夹放进智能体技能目录。

### 方式四：install.sh（多智能体一键脚本）

```text
bash install.sh --agent <name>   # 装到指定智能体默认用户级目录
bash install.sh --dir <path>     # 装到指定目录
bash install.sh --list           # 列出智能体 -> 默认目录
```

> 方式一走 npm 源（npmmirror / npmjs），不依赖 GitHub；方式二 / 三走 GitHub，国内无代理可能失败。

## 开发与校验

技能包自带测试脚本（随发布包一起分发）：

```bash
# 在技能目录内跑全量用例（52 个）
python scripts/test_yotta_verify.py
```

参考资料：`references/injection-patterns.md`（检测模式）、`references/verify-report-template.md`（报告模板）、
`references/badges.md`（徽章说明）。

## 许可证

MIT © YottaMeta —— 见 [LICENSE](./LICENSE)。
