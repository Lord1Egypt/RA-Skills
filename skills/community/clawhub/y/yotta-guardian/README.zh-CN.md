<p align="center"><b>Language</b>: <a href="./README.md">English</a> · 中文</p>


<p align="center">
  <img src="assets/banner.png" alt="yotta-guardian banner" width="100%" />
</p>

<h1 align="center">yotta-guardian · 元盾</h1>

<p align="center">YottaMeta 自有的工具调用拦截护栏：<b>确定性规则引擎 + 可插拔意图验证</b>，对 exec / write / edit / read / run / shell 工具调用做安全评估，输出 allow / deny + 命中规则 + 审计日志。适用于代理要执行高风险命令、写入系统敏感路径、或修改系统配置之前的确定性安全检查。</p>
<p align="center">检测到递归删除、磁盘格式化、提权、防火墙改动、反向 shell、下载即执行、写入系统核心文件等危险操作意图时自动激活——<b>不靠提示词兜底，按规则确定性判定</b>。</p>
<p align="center">纯 Python 3.8+ 标准库实现，零外部依赖；Windows + Linux + macOS 通用；默认只读评估、可配置放行、审计留痕。</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-guardian"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-guardian" /></a>
  <a href="https://github.com/YottaMeta/yotta-guardian"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-guardian" /></a>
  <a href="https://github.com/YottaMeta/yotta-guardian/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-guardian" /></a>
  <a href="https://github.com/YottaMeta/yotta-guardian"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
</p>

## 这是什么

AI 代理在自主执行时，一条递归删除、一次磁盘写入、一段下载即执行，就可能造成不可逆损失。元盾把这些危险动作做成确定性规则引擎：对每一次工具调用（exec / write / edit / read / run / shell）做结构化评估——命令文本、argv 级动词与目标分析、敏感路径、写入内容——给出 allow / deny 判定、命中规则与原因，并支持审计日志留痕。

它不是某个平台的专属功能，而是一份与智能体无关的工具包：装进任何支持 Agent Skills 的智能体即可按需调用。默认只读评估，不自动执行也不放行危险操作；意图验证默认不调用任何模型，可通过协议外接任意验证器（如 LLM 网关）。

## 核心价值

- **确定性规则引擎**：文本模式（下载即执行 / 编码执行 / 反向 shell 等）+ argv 级动词/目标分析（rm / dd / mkfs / chmod / chown / 提权 / 防火墙 / 服务 / 持久化等）+ 敏感路径 + 写入内容，四层规则叠加判定。
- **敏感路径守卫**：/etc/passwd、/etc/sudoers、SSH 授权文件、/boot、/dev 设备、Windows 系统目录与 hosts、注册表启动项等写入即拒。
- **可插拔意图验证（不绑模型）**：默认零依赖；可启用内置本地启发式（--heuristic），也可通过 stdin/stdout JSON 协议外接任意意图验证器（--verifier / 配置文件）。
- **三档策略**：default（拒绝 high+）/ strict（拒绝 medium+）/ loose（仅拒绝 critical），按场景取舍。
- **审计留痕**：JSONL 审计日志 + audit 查询子命令，拒绝/放行全程可追溯。
- **机器可读**：--json 输出纯净 JSON（含逐条判定、规则、退出码），--batch 批量预检，适合智能体在执行前 gate。

## 核心优势

| 优势 | 说明 |
|---|---|
| **零依赖** | Python 3.8+ 标准库，无 daemon / 无数据库 / 无外部扫描器；Windows + Linux + macOS 通用 |
| **确定性** | 规则判定可复现、可解释，不依赖模型概率；意图验证默认关闭，需显式启用 |
| **结构化** | 按工具类型（exec / write / edit / read）分别评估命令、路径与内容，不是简单字符串匹配 |
| **可配置** | --allow / --allow-path / 自定义规则 JSON（policy / deny / allow / verifier） |
| **可追溯** | 每次判定落 JSONL 审计日志，audit 子命令可按拒绝 / 工具 / 时间过滤 |
| **生态分发** | GitHub + npm + ClawHub 三源同步发布；npx / git clone / Download ZIP / install.sh 四种安装方式 |

## 功能体系

| 能力 | 说明 |
|---|---|
| check | 评估一条或一批工具调用（--batch），文本 / JSON / Markdown 报告三种输出 |
| audit | 查询审计日志（--tail / --denied / --since / --tool / --json） |
| rules | 打印内置规则摘要 / 校验自定义规则文件 |
| version | 打印版本 |

## 快速使用

Windows 用 python，Linux/macOS 用 python3。

```bash
# 检查一条 exec（0 = 允许）
python3 scripts/yotta_guardian.py check exec --cmd "git status"

# 检查危险命令（默认拒绝，退出码 3）
python3 scripts/yotta_guardian.py check exec --cmd "rm -rf /"

# 检查写操作（写入 /etc/passwd 被拒）
python3 scripts/yotta_guardian.py check write --path /etc/passwd --content "..."

# 批量预检（agent 在执行前把待执行调用列表交给护栏）
python3 scripts/yotta_guardian.py check --batch calls.json --json

# 审计
python3 scripts/yotta_guardian.py check exec --cmd "..." --audit-log .yotta-guardian/audit.jsonl
python3 scripts/yotta_guardian.py audit --file .yotta-guardian/audit.jsonl --tail 20
```

退出码语义（与元安 / 元审家族一致）：0 = 允许；1 = 允许但带警告（建议人工复核）；2 = 拒绝（high）；3 = 拒绝（critical）；4 = 用法错误 / 致命异常。

## 安装

以下四种方式任选，顺序即推荐优先级；技能文件一律从 **npm** 获取（GitHub 无代理较慢，npm 支持镜像）。

### 方式一：npm 一行装（推荐）

```text
# 可选国内加速：npm config set registry https://registry.npmmirror.com
npx -y @yottameta/yotta-guardian --agent <智能体名称>      # 装到指定智能体默认用户级技能目录
npx -y @yottameta/yotta-guardian --dir <智能体的技能目录>  # 指到技能目录本身（如 ~/.codex/skills）
```

- `--agent <name>` 自动装到该智能体默认用户级目录；`--list` 可查看各智能体默认目录。
- `--dir <路径>` 装到指定的技能目录；未收录的智能体用 `--dir` 指到它的技能目录。
- npmmirror 未同步新包（404）：加 `--registry=https://registry.npmjs.org/`（国内需代理），或稍等镜像缓存。

### 方式二：git clone（开发者 / 有 git 环境）

```text
git clone https://github.com/YottaMeta/yotta-guardian.git <智能体的技能目录>/yotta-guardian
```

### 方式三：GitHub 下载压缩包（手动 / 无 git 环境）

在 GitHub 仓库 `YottaMeta/yotta-guardian` 点 **Code → Download ZIP**，解压后把 `yotta-guardian` 文件夹放进智能体技能目录。

### 方式四：install.sh（多智能体一键脚本）

```text
bash install.sh --agent <name>   # 装到指定智能体默认用户级目录
bash install.sh --dir <path>     # 装到指定目录
bash install.sh --list           # 列出智能体 -> 默认目录
```

> 方式一走 npm 源（npmmirror / npmjs），不依赖 GitHub；方式二 / 三走 GitHub，国内无代理可能失败。
## 使用示例（AI 智能体）

1. 将本仓库的 SKILL.md 接入任意 AI 智能体的技能/规则系统（见上方安装）。
2. 在执行任何高风险工具调用前，先跑一次 check：
   ```bash
   python3 scripts/yotta_guardian.py check exec --cmd "<待执行命令>" --json
   ```
   退出码 2 / 3 时不要执行，向用户说明命中规则；确有授权再用 --allow / --allow-path / 自定义规则放行。
3. 一次要执行多条时，用 --batch 批量预检：
   ```bash
   python3 scripts/yotta_guardian.py check --batch calls.json --json
   ```
4. 写敏感路径 / 修改系统配置前，用 write / edit 检查目标路径与内容。
5. 高风险操作落审计日志，事后用 audit 查询。

## 开发与校验

- 测试：python scripts/test_yotta_guardian.py（60 项）
- 基础校验：python tools/validate-skill.py yotta-guardian（在仓库根目录运行）
- 规则说明：references/rules.md；策略与退出码：references/policies.md；意图验证器协议：references/intent-verifier.md

## 许可证

MIT © YottaMeta —— 详见 [LICENSE](./LICENSE)。

## 致谢

护栏/拦截方向参考开源社区 safe-guardian 类技能思路，实现为 YottaMeta 全新自有代码（详见 [NOTICE](./NOTICE)）。
