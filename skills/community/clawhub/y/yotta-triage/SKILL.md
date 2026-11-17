---
name: yotta-triage
slug: yotta-triage
version: 0.1.6
displayName: 元鉴·样本静态初筛
summary: 恶意样本静态初筛：哈希、魔数、熵、字符串分类与 PE/ELF 解析，输出 triage 报告与 IOC。
description: '元鉴 —— 跨智能体的恶意样本静态初筛技能：零依赖自研对文件 / 目录做纯静态分析（MD5/SHA1/SHA256 哈希、魔数类型识别、Shannon 熵、可打印字符串分类提取、PE/ELF 头解析），输出 triage 报告 + IOC（hash/URL/域/IP/邮箱）供元情消费；只提示可疑、不定性恶意。触发：用户给出可疑文件 / 恶意样本 / 样本目录，要算哈希、识别文件类型、查熵、提取字符串、解析 PE/ELF 头、做静态初筛、产出 IOC 时。边界：只做静态特征，不反混淆、不解包、不动态执行任何样本；不联网查证；仅用于已获授权 / 自有资产 / 教学环境的安全分析。'
tags: [样本分析, 静态初筛, 哈希, IOC, triage, 恶意样本]
category: it-ops-security
license: MIT
homepage: https://github.com/YottaMeta/yotta-triage
---
# 元鉴（yotta-triage）

跨智能体的恶意样本静态初筛技能：零依赖自研对**文件 / 目录**做**纯静态**特征分析——
**MD5/SHA1/SHA256 哈希、魔数类型识别、Shannon 熵、可打印字符串分类提取、PE/ELF 头解析**，
输出 **triage 报告 + IOC（hash / URL / 域 / IP / 邮箱）** 供元情（yotta-intel）消费。

纯 Python 3.8+ 标准库实现，零外部依赖；Windows + Linux + macOS 通用。
**纯本地离线、只读**：不反混淆、不解包、不动态执行任何样本。

## 何时使用

- 用户给出一个可疑文件 / 恶意样本，要快速算哈希、识别文件类型、看熵、提取字符串；
- 要解析 PE / ELF 头（架构、时间戳、区段、加壳线索），判断样本是不是加壳 / 高熵载荷；
- 要对一批样本目录做静态初筛，按风险线索排序，产出 IOC（hash / URL / 域 / IP / 邮箱）供后续分析；
- 恶意样本分析、应急响应、红蓝对抗复盘时需要「先静态看一眼」的环节。

**Do NOT trigger**：
- 不反混淆、不解包、不动态执行任何样本（红线）；
- 不联网查证 IOC 是否恶意、不查询威胁情报平台；
- 不在无授权情况下分析他人样本；仅用于已获授权 / 自有资产 / CTF / 教学环境。

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

# 跳过字符串提取（只算哈希 / 类型 / 熵 / PE-ELF 头；报告显示“已跳过”而不是 0 条）
python3 scripts/yotta_triage.py triage --path sample.exe --no-strings

# 版本
python3 scripts/yotta_triage.py --version
```

退出码：**0** = 最高风险 ≤ low；**1** = medium；**2** = high；**3** = critical；**4** = 用法或读取错误。

## 工作流程（AI 智能体执行样本初筛时）

1. **确认范围**：明确要分析的样本文件 / 目录；只读本地，不做任何外部动作。
2. **读取**：用 triage --path 指向文件或目录；目录可加 --recursive 递归。
3. **静态分析**：引擎流式计算哈希（大文件不吃内存），对分析窗口做魔数识别、熵、
   字符串提取与分类、PE/ELF 头解析。
4. **分级**：按静态指标加权给出 info/low/medium/high/critical 的**线索级**提示。
5. **报告**：text / JSON / Markdown 三种输出；--ioc-only 直接产出 IOC 供元情消费。
6. **决策纪律**：结果只是「可疑线索」，是否恶意需人工 / 其他情报源核实；工具本身不做任何执行。

## 功能

- **哈希**：MD5 / SHA1 / SHA256（流式计算，支持大文件）；
- **类型识别**：魔数识别 PE / ELF / Mach-O / PDF / ZIP / gzip / 7z / RAR / OLE / 图片 / pyc / Java class，
  另含 UTF-8 文本 / shebang 脚本识别；
- **熵**：整体 Shannon 熵 + PE 区段熵（加壳 / 加密 / 压缩线索）；
- **字符串**：可打印字符串（ASCII + UTF-16LE），分类提取 **URL / 域名 / IP / 邮箱 / 可疑命令 / 路径 / 长 base64**；
- **PE 头解析**：机器类型 / 时间戳 / 可选头 / 区段表（名称、特性、熵），识别加壳区段（UPX 等）与 RWX 区段；
- **ELF 头解析**：位宽 / 字节序 / 机器 / 类型 / 入口 / 程序头与节头，识别 RWE 段与 RWX 节；
- **风险分级**：静态指标加权给出线索级风险（评分 + 理由），只提示、不定性；
- **IOC 输出**：hash / URL / 域 / IP / 邮箱汇总，JSON 供元情（yotta-intel）消费；
- **三种输出**：文本 / JSON（stdout 纯净）/ Markdown 报告。

## 风险分级一览

| 级别 | 含义 | 常见触发 |
|---|---|---|
| info | 无明显异常 | 普通文本 / 无风险线索的样本 |
| low | 低风险线索 | 少量 URL / 单条可疑命令 / 轻度高熵 |
| medium | 中等风险线索 | 整体高熵（≥6.5）、疑似加壳区段、ELF RWE 段、多条可疑命令 |
| high | 高风险线索 | 加壳 + 内嵌 URL、多类可疑命令 + 可执行文件、RWX 区段叠加 |
| critical | 严重风险线索 | 加壳 + RWX + 高熵区段 + 下载执行命令等多项叠加 |

> 分级是**静态线索**，不代表样本确定恶意；最终判定需人工 / 动态分析 / 情报交叉验证。

## 输出格式

- **text** — 每文件一段（哈希 / 类型 / 熵 / PE-ELF / 字符串统计 / 风险理由）+ 文件级 IOC 汇总；
- **json** — 结构为 {tool, version, generated, summary, files[], iocs[]}；files[] 每条含
  hashes / type / entropy / strings / pe|elf / risk，iocs[] 为 {type, value, file}（供元情消费）；
- **markdown** — text 报告的围栏包装；
- **--ioc-only** — 只输出 iocs[] JSON 数组。

## 边界（安全红线）

- **纯静态**：只做静态特征，不反混淆、不解包、不动态执行任何样本；
- **只读本地**：不联网查证、不下载、不修改 / 删除任何样本文件；
- **不给定性**：所有风险分级只是「可疑线索」，是否恶意需人工 / 其他情报源核实；
- **授权**：仅用于已获明确授权 / 自有资产 / CTF 靶场 / 教学环境；未经授权分析他人样本违反法律，使用者自行承担责任。

## 参考文档

- references/triage-spec.md — 静态初筛规范（分析项 / 魔数表 / PE-ELF 字段 / 字符串分类）
- references/risk-model.md — 风险分级模型（指标加权 / 阈值 / 与元情 IOC 衔接）

## 法律声明

本技能仅用于**已获明确授权**的安全分析（自有资产、授权测试、CTF 靶场、教学环境）。
未经授权分析他人系统 / 样本数据违反中国《网络安全法》与《刑法》相关条款，使用者自行承担法律责任。
