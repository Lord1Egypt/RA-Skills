---
name: yotta-recon
slug: yotta-recon
version: 0.1.10
displayName: 元析·资产侦察
summary: 授权范围内的资产侦察：端口、服务、版本指纹探测，内建授权纪律 Scope Guard。
description: '元析 —— 跨智能体的网络侦察技能：零依赖自研端口 / 服务 / 版本指纹探测（不依赖 nmap），为安全测试与资产盘点提供侦察能力，内建授权纪律（Scope Guard）。触发：扫描网络 / 端口扫描 / 服务识别 / 版本指纹 / 资产盘点 / CDN 溯源 / 安全测试侦察阶段。边界：仅扫描已获明确授权的目标（红线：授权纪律）；只读探测，不主动攻击、不渗漏、不产生破坏；不用于非法入侵。'
tags: [资产侦察, 端口识别, 指纹探测, 授权范围, recon, 侦察]
category: it-ops-security
license: MIT
homepage: https://github.com/YottaMeta/yotta-recon
---
# 元析（yotta-recon）

跨智能体的网络侦察技能：零依赖自研端口 / 服务 / 版本指纹探测，为安全测试与资产盘点提供侦察能力，内建授权纪律（Scope Guard）。

纯 Python 3.8+ 标准库实现，零外部依赖；Windows + Linux + macOS 通用。

## 何时使用

- 扫描网络 / 端口扫描 / 服务识别 / 版本指纹 / 资产盘点 / CDN 溯源 / 安全测试侦察阶段；
- 需要了解目标开放端口与常见服务版本；
- 做攻击面盘点前先摸清暴露面。

**Do NOT trigger**：
- 不扫描未经明确授权的目标（红线：授权纪律，Scope Guard 默认拒绝）；
- 不主动攻击、不渗漏、不产生破坏；
- 不用于非法入侵；未经授权扫描他人系统违反《网络安全法》与《刑法》第 285/286 条。

## 快速使用

Windows 用 python，Linux/macOS 用 python3。

```bash
# 扫描本机回环（默认放行，无需授权）
python3 scripts/yotta_recon.py scan --targets 127.0.0.1 --top 100

# 有授权范围文件（Scope Guard 声明授权）
python3 scripts/yotta_recon.py scan --targets 192.168.1.0/30 --scope scope.txt --yes

# 用户明确声明已获授权
python3 scripts/yotta_recon.py scan --targets <目标> --assume-authorized --yes

# 单端口深度指纹
python3 scripts/yotta_recon.py fingerprint --host 127.0.0.1 --port 80

# 授权预检（AI 先 check 再 scan）
python3 scripts/yotta_recon.py check-scope --targets <目标> --scope scope.txt

# 本机监听端口清单（只读）
python3 scripts/yotta_recon.py local

# JSON 输出 / Markdown 报告
python3 scripts/yotta_recon.py scan --targets 127.0.0.1 --json
python3 scripts/yotta_recon.py scan --targets 127.0.0.1 --report report.md
```

## 工作流程（AI 智能体执行侦察时）

1. **确认授权**：用户明确给出目标与授权（口头/书面）；优先让用户提供 --scope 授权文件。
2. **预检**：先跑 check-scope，全部 ALLOW 才继续；出现 DENY 先补授权，不绕过。
3. **扫描**：按范围与深度选择端口集（--ports 自定义 / --top N 常用端口），必要时 --rate 限速。
4. **分析**：按风险等级（high/medium/low/none）排序核对；区分「已知版本指纹提示」与「确认漏洞」——指纹提示需人工核实。
5. **报告**：--report 生成 Markdown 报告（含 scan_id / 时间 / 授权来源，操作留痕）；向用户报告发现与建议。
6. **决策纪律**：只做侦察与报告；不主动攻击、不利用、不写入目标系统。

## 功能

- **端口扫描**：TCP connect，并发可调（--concurrency）、可限速（--rate）、超时可调（--timeout）；
- **目标解析**：IP / CIDR / 主机名 / 目标文件，逗号分隔；
- **服务指纹**：banner grab + 协议探测（HTTP / SSH / FTP / SMTP / POP3 / IMAP / Redis / MySQL / PostgreSQL / TLS / MongoDB）；
- **版本提取与风险提示**：内置已知风险映射，命中时标注风险等级并提示「请人工核实」，不提供利用细节；
- **三种输出**：文本表格 / JSON（stdout 纯净）/ Markdown 报告；
- **本机清单**：local 子命令读取本机监听端口（只读）。

## Scope Guard（安全边界）

- **默认拒绝**：仅回环地址（127.0.0.0/8、::1、localhost）默认放行；公网 / 未授权私有 / 保留地址默认拒绝（退出码 3）；
- **授权声明**：--scope 授权文件（IP/CIDR/主机名每行一个，# 注释）或 --assume-authorized --yes；
- **交互确认**：人类直接运行时，未声明授权会提示确认，输入 y 才继续；AI 场景（无输入）自动拒绝；
- **只读**：全部操作为连接/读取，无写入、无删除、无破坏；
- **留痕**：报告含 scan_id、时间、目标、授权来源。

详细规则见 references/scope-guard.md。

## 参考文档

- references/scope-guard.md — 授权纪律五道防线与使用姿势
- references/service-fingerprints.md — 指纹识别规则与已知风险映射
- references/protocol-probes.md — 协议探测实现说明

## 法律声明

本技能仅用于**已获明确授权**的目标（自有资产、授权测试、CTF 靶场、教学环境）。
未经授权扫描他人系统违反中国《网络安全法》与《刑法》第 285/286 条，使用者自行承担法律责任。
