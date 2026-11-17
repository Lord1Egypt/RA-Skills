<p align="center"><b>语言</b>: <a href="./README.md">English</a> · 中文</p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-triage banner" width="100%" />
</p>

<h1 align="center">yotta-triage · 元鉴</h1>

<p align="center">YottaMeta 自研零依赖 <b>恶意样本静态初筛引擎</b>：哈希（<b>MD5 / SHA1 / SHA256</b>）、魔数类型识别、<b>Shannon 熵</b>、可打印字符串分类提取（<b>URL / 域名 / IP / 邮箱 / 可疑命令 / 路径 / base64</b>）、<b>PE / ELF 头解析</b>，输出 triage 报告 + <b>IOC 清单</b>供下游情报消费。</p>
<p align="center">用户给出可疑文件 / 样本（或样本目录）、需要算哈希、识别文件类型、查熵、提取字符串、解析 PE/ELF 头、做静态初筛、产出 IOC 时触发 —— <b>纯本地离线：不反混淆、不解包、不动态执行、不联网查证</b>。</p>
<p align="center">无需外部工具（Python 3.8+ 标准库）；Windows + Linux + macOS 通用；每条结果都是线索提示，绝不定性。</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-triage"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-triage" /></a>
  <a href="https://github.com/YottaMeta/yotta-triage"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-triage" /></a>
  <a href="https://github.com/YottaMeta/yotta-triage/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-triage" /></a>
  <a href="https://github.com/YottaMeta/yotta-triage"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
</p>

## 这是什么

恶意样本分析几乎总是从「这文件是什么？不运行它先看看长相」开始。元鉴把这个环节做成零依赖引擎：算哈希、按魔数识别类型、量 Shannon 熵、提取并分类可打印字符串、解析 PE/ELF 头——只靠 Python 标准库。不需要 YARA、沙箱或专用恶意软件平台。

不绑定任何平台：任何支持 Agent Skills 的智能体都能用。**纯本地离线**——不反混淆、不解包、不动态执行、不联网查证、无常驻服务。

## 核心价值

- **零依赖引擎** — 哈希 + 类型识别 + 熵 + 字符串 + PE/ELF 解析，全用 Python 3.8+ 标准库实现；
- **流式哈希** — MD5 / SHA1 / SHA256 分块计算，大文件不吃内存；
- **类型识别** — 魔数识别 PE / ELF / Mach-O / PDF / ZIP / gzip / 7z / RAR / OLE / 图片 / pyc / Java class，另含 UTF-8 文本与 shebang 脚本；
- **熵** — 整体 Shannon 熵 + PE 逐区段熵（加壳 / 加密 / 压缩线索）；
- **字符串智能** — ASCII + UTF-16LE 可打印字符串，分类成 URL / 域名 / IP / 邮箱 / 可疑命令 / 路径 / 长 base64；
- **PE / ELF 解析** — 架构、时间戳、可选头、区段表（名称 / 特性 / 熵），加壳区段与 RWX 区段检测；ELF 段 / 节 RWE 检测；
- **风险线索而非结论** — 静态指标加权产出 info/low/medium/high/critical 线索（评分 + 理由），绝不执行样本；
- **IOC 输出** — hash / URL / 域 / IP / 邮箱汇总为 JSON，直接给元情（yotta-intel）与其它情报管线消费；
- **三种输出** — text / JSON / Markdown，外加 --ioc-only。

## 为什么用

| 优势 | 说明 |
|---|---|
| **零依赖** | Python 3.8+ 标准库；无守护进程 / 数据库 / YARA / 沙箱；Windows + Linux + macOS |
| **纯本地离线** | 只读分析已有文件；不反混淆、不解包、不执行、不联网 |
| **可解释** | 每条风险线索带评分与中文理由；绝不给裸结论 |
| **低噪音** | 非 TLD 后缀过滤（payload.exe 不算域名）、IP 八位组校验、去重 |
| **下游友好** | --ioc-only 直接输出干净的 IOC JSON 数组，供元情与其它情报管线使用 |
| **生态分发** | GitHub + npm + ClawHub 三源同步；npx / git clone / Download ZIP / install.sh 四种安装方式 |

## 命令

| 命令 | 说明 |
|---|---|
| triage --path <文件\|目录> | 对单个文件或目录做静态初筛 |
| triage --recursive | 扫描目录时递归子目录 |
| triage --format | 输出格式：text（默认）/ json / markdown |
| triage --output <文件> | 报告写入文件（默认 stdout） |
| triage --ioc-only | 只输出 IOC JSON 数组（供元情） |
| triage --no-strings | 跳过字符串提取；报告显示“已跳过”，不把未提取误报成 0 条 |
| triage --strings-min <n> | 可打印字符串最小长度（默认 4） |
| triage --strings-limit <n> | 每文件字符串提取上限（默认 500） |
| triage --max-file-mb <n> | 超过该大小(MB)的文件跳过（默认 256） |

退出码：**0** = 最高风险 ≤ low；**1** = medium；**2** = high；**3** = critical；**4** = 用法或读取错误。

## 快速使用

Windows 用 python，Linux/macOS 用 python3。

```bash
# 分析单个样本（文本报告）
python3 scripts/yotta_triage.py triage --path sample.exe

# 分析目录（递归子目录）
python3 scripts/yotta_triage.py triage --path samples/ --recursive

# JSON 报告
python3 scripts/yotta_triage.py triage --path sample.exe --format json --output report.json

# Markdown 报告
python3 scripts/yotta_triage.py triage --path samples/ --format markdown --output report.md

# 只输出 IOC（hash / URL / 域 / IP / 邮箱），供元情消费
python3 scripts/yotta_triage.py triage --path samples/ --ioc-only --output iocs.json

# 版本
python3 scripts/yotta_triage.py --version
```

文本输出示例：

```
=== 元鉴 yotta-triage 静态初筛报告 ===
工具: yotta-triage v0.1.1 | 生成: 2026-08-28T00:00:00+00:00
文件: 2（成功 2）| 最高风险: medium | IOC: 5 条

:: sample_upx.exe  (DOS/PE executable (MZ), 4776 bytes)
  MD5   : 8440cd803c0ae8c092da448b2fa810d8
  SHA256: b90093fbae4e34ce410bd63fc203dbd88d94b38f54a7c1f9acca635b12efa203
  熵     : 0.184（全文）
  PE    : PE32+ | x86-64 | 时间戳 2021-05-03 00:00:00 UTC | 区段 2
    - .text     R-X 熵 0.36
    - .UPX0     RW- 熵 0.11
  字符串: 3 条 | 1 URL | 1 域 | 0 IP | 0 邮箱 | 0 命令 | 0 base64
    URL  : http://download.example.net/a.exe
  风险 : 中等风险线索（评分 4）
    - 疑似加壳区段: .UPX0
    - 可执行文件内嵌 URL（1 条）
```

## 安装

以下四种方式任选，顺序即推荐优先级；技能文件一律从 **npm** 获取（GitHub 无代理较慢，npm 支持镜像）。

### 方式一：npm 一行装（推荐）

```text
# 可选国内加速：npm config set registry https://registry.npmmirror.com
npx -y @yottameta/yotta-triage --agent <智能体名称>      # 装到指定智能体默认用户级技能目录
npx -y @yottameta/yotta-triage --dir <智能体的技能目录>  # 指到技能目录本身（如 ~/.codex/skills）
```

- `--agent <name>` 自动装到该智能体默认用户级目录；`--list` 可查看各智能体默认目录。
- `--dir <路径>` 装到指定的技能目录；未收录的智能体用 `--dir` 指到它的技能目录。
- npmmirror 未同步新包（404）：加 `--registry=https://registry.npmjs.org/`（国内需代理），或稍等镜像缓存。

### 方式二：git clone（开发者 / 有 git 环境）

```text
git clone https://github.com/YottaMeta/yotta-triage.git <智能体的技能目录>/yotta-triage
```

### 方式三：GitHub 下载压缩包（手动 / 无 git 环境）

在 GitHub 仓库 `YottaMeta/yotta-triage` 点 **Code → Download ZIP**，解压后把 `yotta-triage` 文件夹放进智能体技能目录。

### 方式四：install.sh（多智能体一键脚本）

```text
bash install.sh --agent <name>   # 装到指定智能体默认用户级目录
bash install.sh --dir <path>     # 装到指定目录
bash install.sh --list           # 列出智能体 -> 默认目录
```

> 方式一走 npm 源（npmmirror / npmjs），不依赖 GitHub；方式二 / 三走 GitHub，国内无代理可能失败。
## 输出格式

- **text** — 每文件一段（哈希 / 类型 / 熵 / PE-ELF / 字符串统计 / 风险理由）+ 文件级 IOC 汇总；
- **json** — 结构为 {tool, version, generated, summary, files[], iocs[]}；files[] 每条含 hashes / type / entropy / strings / pe|elf / risk，iocs[] 为 {type, value, file}（供元情消费）；
- **markdown** — text 报告的围栏包装；
- **--ioc-only** — 只输出 iocs[] JSON 数组。

## 开发与校验

技能包自带测试脚本（随包发布）：

```bash
# 从技能目录运行全部用例（65 个）
python scripts/test_yotta_triage.py
```

规范细节见 references/：triage-spec.md（分析项 / 魔数表 / PE-ELF 字段 / 字符串分类）、risk-model.md（指标加权 / 阈值 / 与元情 IOC 衔接）。

## 许可证

MIT © YottaMeta —— 见 LICENSE。
