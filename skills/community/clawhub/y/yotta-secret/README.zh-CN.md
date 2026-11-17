<p align="center"><b>Language</b>: <a href="./README.md">English</a> · 中文</p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-secret banner" width="100%" />
</p>

<h1 align="center">yotta-secret · 元钥 (Yuanyao)</h1>

<p align="center">YottaMeta 的零依赖密钥 / 凭据泄露源头扫描引擎：用「正则 + 熵 + 格式校验」离线扫描源码 / 配置 / .env / git 历史，覆盖云厂商 API Key、私钥、口令赋值、URL 内嵌凭据与高熵长 token，输出 text / JSON / CSV。</p>
<p align="center">触发场景：提交或发布前排查仓库是否泄露密钥、扫描目录或 git 历史找硬编码凭据源头、校验某字符串是否为已知格式密钥、在分享日志 / 工单前给文本脱敏。</p>
<p align="center">纯 Python 3.8+ 标准库实现，零外部依赖，Windows + Linux + macOS 通用；输出默认打码，防二次泄露。</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-secret"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-secret" /></a>
  <a href="https://github.com/YottaMeta/yotta-secret"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-secret" /></a>
  <a href="https://github.com/YottaMeta/yotta-secret/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-secret" /></a>
  <a href="https://github.com/YottaMeta/yotta-secret"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
</p>

## 这是什么

代码里硬编码的 API Key、密码、私钥是泄露源头：一旦进了 git 历史就很难真正删除。元钥把「密钥排查」打包成零依赖引擎——不需要 gitleaks / trufflehog 等外部工具，只靠 Python 标准库完成 正则 + 熵 + 格式校验 三层判定，帮你在提交、发布、分享前找出疑似密钥。

它与任何平台无关，是智能体无关的工具包，支持 Agent Skills 的智能体都能调用。**纯本地离线**——不联网验证密钥是否有效、不发送任何数据、无常驻服务。

## 核心价值

- **零依赖引擎**——五类检测 + 三重判定，全部用 Python 3.8+ 标准库实现。
- **五类检测**——cloud（云厂商 / SaaS API Key）、private_key（PEM / PGP / OpenSSH / PuTTY 私钥）、credential（口令赋值，含 __MYAPP_SECRET=__ 后缀式 key）、url_userinfo（URL 内嵌账号密码）、generic（高熵长 token）。
- **三重判定**——正则格式 → Shannon 熵阈值 → 值级校验（纯哈希 / UUID / 占位符 / 示例值过滤），误报可控。
- **git 历史扫描**——__--git__ 走 __git log -p__ 只扫新增行，逐条带 commit 与路径，定位泄露源头。
- **默认打码**——输出只保留密钥头尾（如 __ghp_****abcd__），__--show-secret__ 才明文，防二次泄露。
- **三种输出**——text / JSON / CSV，可直接喂给 CI 门禁、元盾审计或人工复核。

## 为什么用它

| 优势 | 说明 |
|---|---|
| **零依赖** | Python 3.8+ 标准库；无守护进程 / 无数据库 / 无外部扫描器；Windows + Linux + macOS |
| **纯本地离线** | 只扫描已存在的文件与文本；不联网验证、不发送任何数据 |
| **误报可控** | 占位符 / 示例值 / 环境变量引用过滤，纯哈希与 UUID 排除，中等置信 key 需更长或更高熵 |
| **源头定位** | git 历史扫描逐条带 commit 与路径，不只是「有泄露」而是「哪次提交引入」 |
| **防二次泄露** | 输出默认打码；mask 子命令可直接给日志 / 工单脱敏（与元史同源） |
| **生态分发** | GitHub + npm + ClawHub 三源同步；npx / git clone / Download ZIP / install.sh 四种安装方式 |

## 命令

| 命令 | 说明 |
|---|---|
| scan | 扫描文件 / 目录 / stdin / git 历史中的疑似密钥 |
| scan --path / --stdin | 输入来自文件 / 标准输入 |
| scan --git | 扫描 git 历史（新增行，带 commit） |
| scan --types | 只检测指定类别（cloud,private_key,credential,url_userinfo,generic） |
| scan --format | 输出格式（text / json / csv） |
| scan --show-secret | 明文显示密钥（默认打码） |
| scan --exclude | 排除路径模式（fnmatch，可多次） |
| scan --output | 结果写入文件（默认 stdout） |
| verify | 校验单个值是否为疑似密钥（--value / --stdin） |
| mask | 把文本中疑似密钥打码（与元史脱敏同源） |
| entropy | 计算 Shannon 信息熵 |
| --version | 显示版本 |

## 快速开始

### 安装

以下四种方式任选，顺序即推荐优先级；技能文件一律从 **npm** 获取（GitHub 无代理较慢，npm 支持镜像）。

#### 方式一：npm 一行装（推荐）

```text
# 可选国内加速：npm config set registry https://registry.npmmirror.com
npx -y @yottameta/yotta-secret@0.2.4 --agent <智能体名称>      # 装到指定智能体默认用户级技能目录
npx -y @yottameta/yotta-secret@0.2.4 --dir <智能体的技能目录>  # 指到技能目录本身（如 ~/.codex/skills）
```

- `--agent <name>` 自动装到该智能体默认用户级目录；`--list` 可查看各智能体默认目录。
- `--dir <路径>` 装到指定的技能目录；未收录的智能体用 `--dir` 指到它的技能目录。
- npmmirror 未同步新包（404）：加 `--registry=https://registry.npmjs.org/`（国内需代理），或稍等镜像缓存。

#### 方式二：git clone（开发者 / 有 git 环境）

```text
git clone https://github.com/YottaMeta/yotta-secret.git <智能体的技能目录>/yotta-secret
```

#### 方式三：GitHub 下载压缩包（手动 / 无 git 环境）

在 GitHub 仓库 `YottaMeta/yotta-secret` 点 **Code → Download ZIP**，解压后把 `yotta-secret` 文件夹放进智能体技能目录。

#### 方式四：install.sh（多智能体一键脚本）

```text
bash install.sh --agent <name>   # 装到指定智能体默认用户级目录
bash install.sh --dir <path>     # 装到指定目录
bash install.sh --list           # 列出智能体 -> 默认目录
```

> 方式一走 npm 源（npmmirror / npmjs），不依赖 GitHub；方式二 / 三走 GitHub，国内无代理可能失败。

Windows 用 python，Linux/macOS 用 python3。

```bash
# 扫描目录（递归，自动跳过 .git / node_modules / 二进制）
python3 scripts/yotta_secret.py scan --path src/

# 从标准输入读取，输出 JSON
cat dump.txt | python3 scripts/yotta_secret.py scan --stdin --format json

# 只扫云厂商密钥与私钥
python3 scripts/yotta_secret.py scan --path . --types cloud,private_key

# 扫描 git 历史（新增行），输出 CSV
python3 scripts/yotta_secret.py scan --git --path repo/ --format csv --output report.csv

# 校验单个值是否为疑似密钥
python3 scripts/yotta_secret.py verify --value ghp_xxxxxxxxxxxxxxxx

# 把文本中的疑似密钥打码
python3 scripts/yotta_secret.py mask --path notes.txt --output safe.txt
```

退出码：**scan 0** = 未发现；**1** = 发现疑似密钥；**4** = 用法 / 读取 / git 不可用错误。
verify 命中规则返回 1，未命中返回 0。

### 与元史（yotta-logs）联动

- 元钥负责**源头**：提交 / 发布前扫描源码与 git 历史，找出泄露的密钥；
- 元史负责**输出**：检索会话日志时默认脱敏（redact），避免日志里再次带出密钥；
- 两者词库同源：元钥 mask 子命令的脱敏行为与元史一致，本引擎规则为其超集。规则对照见 references/integration.md。

### 与元盾（yotta-guardian）联动

- 在写入 / 提交前先跑 `scan`：退出码 1 = 发现疑似密钥 → 拦截并提示人工处理；
- `scan --format json` 的结果可直接交给元盾做审计留痕，或接入 CI 门禁：
  ```bash
  python3 scripts/yotta_secret.py scan --path . --format json --output secret-report.json
  # 退出码非 0 时终止提交 / 构建
  ```

## 检测类型

| 类别 | 中文 | 示例 | 说明 |
|---|---|---|---|
| cloud | 云厂商 / SaaS 密钥 | `AKIA…` `ghp_…` `sk-…` `eyJ…` | AWS / Google / OpenAI / GitHub / Slack / Stripe / JWT 等 20+ 规则 |
| private_key | 私钥 | `-----BEGIN RSA PRIVATE KEY-----` | PEM / PGP / OpenSSH / PuTTY 私钥块 |
| credential | 凭据赋值 | `DB_PASSWORD=…` `api_key=…` | 高置信 key 名 + 非占位值（含后缀式 key） |
| url_userinfo | URL 内嵌凭据 | `https://admin:hunter2@…` | URL userinfo 携带账号密码 |
| generic | 高熵长 Token | 40+ 位高熵字符串 | 无前缀但熵达标的兜底检测（medium，人工复核） |

完整规则目录见 references/rules.md；熵阈值与格式校验规范见 references/entropy-and-verification.md。

## 输出格式

- **text**：按类别分组的可读报告（严重度 / 文件行号 / 密钥打码 / 熵 / 上下文）；
- **json**：`{tool, version, generated, source, summary, findings[], rules[]}`，findings 含 `rule_id / rule_name / category / severity / file / line / secret / entropy / length / snippet / commit`；
- **csv**：`rule_id,rule_name,category,severity,file,line,secret,entropy,length,snippet,commit,path_in_commit`。

## 边界（安全红线）

- **纯本地离线**：不联网验证密钥是否有效、不查询泄露库、不发送任何数据；
- **不给定性**：所有结果只是「疑似密钥」，是否真实需人工核实；处理建议（轮换 / 移入密钥管理 / 清理历史）由用户决定；
- **授权**：仅用于已获明确授权 / 自有资产 / 教学环境；未经授权扫描他人数据违反法律，使用者自行承担责任。

## 开发与验证

技能包内自带测试（含在 npm 包 files 中）：

```bash
python scripts/test_yotta_secret.py   # 91 项测试（Windows 用 python）
```

修改引擎后请保持测试全绿，再升版本发布。

## 版本记录

见 [CHANGELOG.md](./CHANGELOG.md)。

## 许可证

[MIT](./LICENSE) © YottaMeta。「元钥」「yotta-secret」及 YottaMeta 家族名称（yotta-* 前缀）为 YottaMeta 品牌标识，派生作品不得继续使用，详见 [NOTICE](./NOTICE)。
