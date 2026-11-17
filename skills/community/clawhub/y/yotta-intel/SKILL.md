---
name: yotta-intel
slug: yotta-intel
version: 0.2.4
displayName: 元情·威胁情报提取
summary: 威胁情报 IOC 提取：从文本、日志提取 IP、域名、URL、哈希与 CVE，去重归一化输出。
description: '元情 —— 跨智能体的威胁情报 IOC 提取与规范化技能：零依赖自研从文本 / 日志 / 报告中提取 IP（IPv4/IPv6）、域名、URL、邮箱、哈希（MD5/SHA1/SHA256/SHA512）与 CVE 编号，识别并还原 defang 写法，去重、归一化后输出 CSV / JSON / STIX-lite。触发：用户给出含可疑 IP / 域名 / URL / 哈希的威胁情报文本、恶意样本分析报告、钓鱼邮件或日志，要提取 IOC、规范化、去重、转格式、共享情报时。边界：纯本地离线提取与规范化；不联网查证、不下载样本、不主动扫描任何系统；仅用于已获授权 / 自有资产 / 教学环境的安全分析。'
tags: [威胁情报, IOC提取, 安全情报, 归一化, threat intel, 检测]
category: it-ops-security
license: MIT
homepage: https://github.com/YottaMeta/yotta-intel
---
# 元情（yotta-intel）

跨智能体的威胁情报 IOC 提取与规范化技能：零依赖自研从**威胁情报文本 / 安全报告 / 钓鱼邮件 / 日志**中提取
**IP（IPv4/IPv6）、域名、URL、邮箱、哈希（MD5/SHA1/SHA256/SHA512）与 CVE 编号**，
自动识别 defang（去活性）写法并还原，去重、归一化后输出 **CSV / JSON / STIX-lite**。

纯 Python 3.8+ 标准库实现，零外部依赖；Windows + Linux + macOS 通用。
**纯本地离线处理**：不联网查证、不下载样本、不主动扫描任何系统。

## 何时使用

- 用户给出一段威胁情报 / 恶意样本分析报告 / 钓鱼邮件 / 日志，要提取其中的 IOC；
- 要批量归一化、去重一堆 IP / 域名 / 哈希，或把 defang 文本还原成规范形态；
- 要把 IOC 整理成 CSV / JSON，或转成 STIX 2.1 Indicator 供平台导入；
- 要在邮件 / 群聊 / 工单里安全共享 IOC（defang 防误点）之前做一次清洗。

**Do NOT trigger**：
- 不联网查证 IOC 是否恶意、不查询威胁情报平台、不下载样本；
- 不主动扫描网络 / 主机，只处理**已存在**的文本内容；
- 不在无授权情况下用于对抗他人系统；仅用于已获授权 / 自有资产 / 教学环境的安全分析。

## 快速使用

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

退出码：**0** = 无 IOC（extract）；**1** = 发现 IOC（extract）；**4** = 用法或读取错误。
defang / refang 成功均为 **0**。

## 工作流程（AI 智能体执行 IOC 提取时）

1. **确认范围**：明确要处理的文本 / 文件与需要的 IOC 类型；纯本地文本，不做任何外部动作。
2. **读取**：用 `extract --path` 指向文件，或 `--stdin` 从管道读取。
3. **提取**：引擎自动 refang 预处理 → 逐行提取七类 IOC → 归一化（小写 / IDN punycode / 去默认端口等）。
4. **去重**：同一 IOC 只保留一条，记录出现次数、首次行号与上下文；`--min-count` 过滤低频噪音。
5. **输出**：text / JSON / CSV / STIX-lite 四种格式；`--output` 写文件，默认打印。
6. **决策纪律**：结果只是「候选指标」，是否恶意需人工 / 其他情报源核实；共享时用 defang 形态防误点。

## 功能

- **七类 IOC 提取**：IPv4、IPv6、域名、URL、邮箱、哈希（MD5/SHA1/SHA256/SHA512）、CVE 编号；
- **defang / refang**：识别 `hxxp`、`[.]`、`(.)`、`[dot]`、`[:]`、`[@]`、`[/]` 等常见去活性写法并还原；
  每条结果自带统一的 defang 安全形态；
- **归一化**：域名小写 + IDN punycode、URL 去默认端口 / 去 fragment / 保留 userinfo、哈希小写、IPv6 压缩写法、
  IPv4-mapped IPv6 规范化；
- **误报控制**：域名 TLD 白名单 + 文件名过滤（`README.md` / `test.py` 不算域名）+ 中文标点截断 + 哈希长度校验；
- **去重计数**：以 `(类型, 规范值)` 为键合并，记录 `count` / `first_line` / `snippet`；
- **四种输出**：文本 / JSON（stdout 纯净）/ CSV / STIX-lite（STIX 2.1 Bundle + indicator pattern，uuid5 确定性）。

详细的类型判定、defang 与 STIX 映射见 references/。

## IOC 类型一览

| 类型 | 中文 | 示例 | 说明 |
|---|---|---|---|
| ipv4 | IPv4 地址 | `203.0.113.5` | 合法八位组；前导零归一 |
| ipv6 | IPv6 地址 | `2001:db8::1` | 压缩写法；IPv4-mapped 输出规范十六进制 |
| domain | 域名 | `evil.example.com` | TLD 白名单；IDN 转 punycode；`README.md` 不算域名 |
| url | URL | `http://evil.example.com/a` | http/https/ftp；去默认端口与 fragment |
| email | 邮箱 | `admin@example.com` | 域名段校验；defang 形态 `admin[@]example[.]com` |
| hash | 哈希 | `44d886…2f` | 仅 32/40/64/128 位十六进制 |
| cve | CVE 编号 | `CVE-2024-1234` | 统一大写 |

## 输出格式

- **text**：按类型分组的可读报告（含 defang 形态与首次出现的上下文）；
- **json**：`{tool, version, generated, source, summary, indicators[]}`，`indicators` 每条含
  `type / value / defanged / count / first_line / snippet`；
- **csv**：`type,value,defanged,count,first_line,snippet`；
- **stix**：STIX 2.1 Bundle，每条 IOC 生成一个 `indicator`（pattern + `x_yottameta_*` 扩展属性）。

## 边界（安全红线）

- **纯本地离线**：不联网查证、不下载样本、不主动扫描任何系统，只做文本提取与规范化；
- **不给定性**：所有 IOC 只是「候选指标」，是否恶意需人工 / 其他情报源核实；
- **授权**：仅用于已获明确授权 / 自有资产 / 教学环境的安全分析；未经授权分析他人数据违反法律，使用者自行承担责任。

## 参考文档

- references/ioc-spec.md — IOC 类型与判定规则（归一化 / 误报控制 / 已知取舍）
- references/defang-rules.md — defang / refang 规则与安全共享建议
- references/stix-lite-spec.md — STIX-lite 输出规范与 pattern 映射

## 常见问题（速查）

装不上、提取为空、defang 没还原、退出码看不懂时，先看 references/faq.md（含速查索引与安装排障）。

## 法律声明

本技能仅用于**已获明确授权**的安全分析（自有资产、授权测试、CTF 靶场、教学环境）。
未经授权分析他人系统数据违反中国《网络安全法》与《刑法》相关条款，使用者自行承担法律责任。
