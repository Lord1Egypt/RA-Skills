<p align="center"><b>Language</b>: <a href="./README.md">English</a> · 中文</p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-intel banner" width="100%" />
</p>

<h1 align="center">yotta-intel · 元情 (Yuanqing)</h1>

<p align="center">YottaMeta 的零依赖威胁情报 IOC 提取与规范化引擎：从威胁情报文本 / 安全报告 / 钓鱼邮件 / 日志中提取
<b>IP（IPv4/IPv6）、域名、URL、邮箱、哈希（MD5/SHA1/SHA256/SHA512）与 CVE 编号</b>，
识别并还原 defang（去活性）写法，去重、归一化后输出 <b>CSV / JSON / STIX-lite</b>。</p>
<p align="center">触发场景：用户给出含可疑 IP / 域名 / URL / 哈希的情报文本，要提取 IOC、规范化、去重、转格式或安全共享时 —
<b>纯本地离线，不联网查证、不下载样本、不主动扫描任何系统</b>。</p>
<p align="center">零外部依赖（Python 3.8+ 标准库）；Windows + Linux + macOS；每条结果自带安全共享用的 defang 形态与中文说明。</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-intel"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-intel" /></a>
  <a href="https://github.com/YottaMeta/yotta-intel"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-intel" /></a>
  <a href="https://github.com/YottaMeta/yotta-intel/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-intel" /></a>
  <a href="https://github.com/YottaMeta/yotta-intel"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
</p>

## 这是什么

威胁情报分析经常从「一堆文本里找指标」开始：这份报告里有哪些可疑 IP？钓鱼邮件里的域名 / 链接是什么？
样本哈希是多少、属于哪种算法？元情把这些能力打包成零依赖引擎——不需要 MISP / OpenCTI / 厂商情报平台，
用纯 Python 标准库就能完成 IOC 提取、defang/refang、去重、归一化与格式转换。

它不是任何单一平台的专属工具：它是一套与智能体无关的工具包，任何支持 Agent Skills 的智能体都能用。
**纯本地离线**——不联网查证、不下载样本、不主动扫描任何系统、无常驻服务。

## 核心价值

- **零依赖引擎**——七类 IOC 提取 + defang/refang + 归一化，全部用 Python 3.8+ 标准库实现；
- **七类 IOC**——IPv4 / IPv6 / 域名 / URL / 邮箱 / 哈希（MD5/SHA1/SHA256/SHA512）/ CVE；
- **defang / refang**——识别 `hxxp`、`[.]`、`(.)`、`[dot]`、`[:]`、`[@]`、`[/]` 等常见去活性写法并还原；
  每条结果自带统一 defang 形态，共享时防误点；
- **去重 + 归一化**——同一 IOC 只保留一条，记录出现次数 / 首次行号 / 上下文；域名小写 + IDN punycode、
  URL 去默认端口、哈希小写、IPv6 压缩写法；
- **四种输出**——text / JSON / CSV / STIX-lite（STIX 2.1 Bundle + indicator pattern）；
- **误报控制**——域名 TLD 白名单 + 文件名过滤（`README.md` / `test.py` 不算域名）+ 中文标点截断 + 哈希长度校验。

## 为什么用它

| 优势 | 说明 |
|---|---|
| **零依赖** | Python 3.8+ 标准库；无守护进程 / 数据库 / 外部扫描器；Windows + Linux + macOS |
| **纯本地离线** | 只处理已存在的文本内容；不联网查证、不下载样本、不主动扫描 |
| **defang 友好** | 识别主流去活性写法并还原；输出统一 defang 形态，安全共享防误点 |
| **可解释** | 每条结果带类型、出现次数、首次行号与上下文；只给「候选指标」，不给定性结论 |
| **低误报** | TLD 白名单 + 文件名过滤 + 中文标点截断等确定性规则 |
| **生态分发** | GitHub + npm + ClawHub 三源同步；npx / git clone / Download ZIP / install.sh 四种安装方式 |

## 命令

| 命令 | 说明 |
|---|---|
| extract | 提取 IOC 并输出结构化结果（text / json / csv / stix） |
| extract --path / --stdin | 指定输入文件 / 从标准输入读取 |
| extract --types | 只提取指定类型（逗号分隔，如 ipv4,domain,hash） |
| extract --format | 切换输出格式（text / json / csv / stix） |
| extract --min-count | 只保留出现次数 >= N 的 IOC |
| extract --output | 结果写入文件（默认打印到 stdout） |
| defang | 把文本中识别到的 IOC 替换为安全 defang 形态 |
| refang | 把 defang 文本还原为原始形态 |
| --version | 打印版本 |

退出码：extract **0** = 无 IOC；**1** = 发现 IOC；**4** = 用法或读取错误；defang / refang 成功均为 **0**。

## 快速上手

Windows 用 python，Linux/macOS 用 python3。

```bash
# 提取文本中的 IOC（默认全部类型，文本输出）
python3 scripts/yotta_intel.py extract --path report.txt

# 从标准输入读取，输出 JSON
cat intel.txt | python3 scripts/yotta_intel.py extract --stdin --format json

# 只提取域名与哈希，且出现次数 >= 2
python3 scripts/yotta_intel.py extract --path intel.md --types domain,hash --min-count 2

# 输出 CSV 供表格 / 平台导入
python3 scripts/yotta_intel.py extract --path intel.md --format csv --output iocs.csv

# 输出 STIX 2.1 Bundle
python3 scripts/yotta_intel.py extract --path intel.md --format stix --output iocs.json

# 把报告转成可安全共享的 defang 版（防误点）
python3 scripts/yotta_intel.py defang --path report.txt --output safe.txt

# 把 defang 情报还原成原始形态
python3 scripts/yotta_intel.py refang --path safe.txt
```

输出示例（text）：

```
元情 yotta-intel v0.2.1 —— IOC 提取结果
共发现 2 个 IOC：

■ IPv4 地址（ipv4）
  203.0.113.5  ×1  行 1
    defang: 203[.]0[.]113[.]5
    上下文: 攻击者从 203.0.113.5 发起请求。
```

## 安装

以下四种方式任选，顺序即推荐优先级；技能文件一律从 **npm** 获取（GitHub 无代理较慢，npm 支持镜像）。

### 方式一：npm 一行装（推荐）

```text
# 可选国内加速：npm config set registry https://registry.npmmirror.com
npx -y @yottameta/yotta-intel@0.2.4 --agent <智能体名称>      # 装到指定智能体默认用户级技能目录
npx -y @yottameta/yotta-intel@0.2.4 --dir <智能体的技能目录>  # 指到技能目录本身（如 ~/.codex/skills）
```

- `--agent <name>` 自动装到该智能体默认用户级目录；`--list` 可查看各智能体默认目录。
- `--dir <路径>` 装到指定的技能目录；未收录的智能体用 `--dir` 指到它的技能目录。
- npmmirror 未同步新包（404）：加 `--registry=https://registry.npmjs.org/`（国内需代理），或稍等镜像缓存。

### 方式二：git clone（开发者 / 有 git 环境）

```text
git clone https://github.com/YottaMeta/yotta-intel.git <智能体的技能目录>/yotta-intel
```

### 方式三：GitHub 下载压缩包（手动 / 无 git 环境）

在 GitHub 仓库 `YottaMeta/yotta-intel` 点 **Code → Download ZIP**，解压后把 `yotta-intel` 文件夹放进智能体技能目录。

### 方式四：install.sh（多智能体一键脚本）

```text
bash install.sh --agent <name>   # 装到指定智能体默认用户级目录
bash install.sh --dir <path>     # 装到指定目录
bash install.sh --list           # 列出智能体 -> 默认目录
```

> 方式一走 npm 源（npmmirror / npmjs），不依赖 GitHub；方式二 / 三走 GitHub，国内无代理可能失败。
## 输出格式

- **text**：按类型分组的可读报告（含 defang 形态与首次出现的上下文）；
- **json**：`{tool, version, generated, source, summary, indicators[]}`，`indicators` 每条含
  `type / value / defanged / count / first_line / snippet`；
- **csv**：`type,value,defanged,count,first_line,snippet`；
- **stix**：STIX 2.1 Bundle，每条 IOC 生成一个 `indicator`（pattern + `x_yottameta_*` 扩展属性），
  详见 `references/stix-lite-spec.md`。

## 开发与校验

技能包内自带测试脚本（随包发布）：

```bash
# 在技能目录内运行全部测试（103 个用例）
python scripts/test_yotta_intel.py
```

规则与规范的细节见 `references/`：ioc-spec.md（类型判定）、defang-rules.md（defang 规则）、
stix-lite-spec.md（STIX 映射）。

## 许可证

MIT © YottaMeta —— 详见 [LICENSE](./LICENSE)。
