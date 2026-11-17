---
name: yotta-logwatch
slug: yotta-logwatch
version: 0.3.3
displayName: 元察·安全日志分析
summary: 安全日志分析检测：解析系统、Web、事件日志，检测爆破、webshell、扫描与异常登录。
description: '元察 —— 跨智能体的安全日志分析检测技能：零依赖自研解析 auth/secure、Web 访问日志（common/combined）、PowerShell 脚本块日志、Windows 事件日志（Security/System），检测爆破 / webshell / 扫描 / 异常登录 / 可疑脚本块 / 可疑进程 / 账户操作 / 日志清空，输出时间线与中文教学报告。触发：用户给出登录日志 / Web 访问日志 / PowerShell 日志 / Windows 事件日志，要分析入侵痕迹、排查异常活动、审计本地日志时。边界：只读本地日志文件；不联网、不主动扫描、不修改任何其内容；仅用于已获授权 / 自有资产的安全审计。'
tags: [日志分析, 异常检测, 安全监控, 爆破检测, log analysis, 检测]
category: it-ops-security
license: MIT
homepage: https://github.com/YottaMeta/yotta-logwatch
---
# 元察（yotta-logwatch）

跨智能体的安全日志分析检测技能：零依赖自研解析 **auth/secure**、**Web 访问日志（common/combined）**、**PowerShell 脚本块日志**、**Windows 事件日志（Security/System）**，检测登录爆破 / webshell / 扫描 / 异常登录 / 可疑脚本块 / 可疑进程 / 账户操作 / 日志清空，输出带中文教学说明的时间线与报告。

纯 Python 3.8+ 标准库实现，零外部依赖；Windows + Linux + macOS 通用。**只读本地日志**，不联网、不主动扫描、不修改任何其内容。

## 何时使用

- 用户给出登录日志（/var/log/auth.log、secure、journal 等）要排查登录爆破 / 异常登录 / sudo 提权；
- 给出 Web 访问日志（nginx / apache common|combined）要排查扫描 / webshell / 路径遍历 / SQL 注入 / 可疑 UA；
- 给出 PowerShell 脚本块日志要排查编码命令 / 下载执行 / 反射加载 / AMSI 绕过 / 混淆；
- 给出 Windows 事件日志（Security/System，key=value / wevtutil 文本 / XML 导出）要排查登录爆破 / 异常登录 / 账户操作 / 日志清空 / 可疑进程；
- 安全测试、应急响应、红蓝对抗后需要「对本地日志做只读审计」时。

**Do NOT trigger**：
- 不主动扫描网络 / 主机，只分析**已存在**的日志文件；
- 不联网拉取情报、不主动连接目标、不修改或删除任何日志内容；
- 不在无授权情况下用于对抗他人系统；仅用于已获授权 / 自有资产 / CTF / 教学环境的安全审计。

## 快速使用

Windows 用 python，Linux/macOS 用 python3。

```bash
# 分析本地 auth 日志
python3 scripts/yotta_logwatch.py scan --path /var/log/auth.log

# 递归扫描目录下所有日志特征文件，输出 Markdown 报告
python3 scripts/yotta_logwatch.py scan --path /var/log/nginx --recursive --report report.md

# 强制指定日志类型为 Web
python3 scripts/yotta_logwatch.py scan --path access.log --type web

# 只显示 medium 及以上严重度
python3 scripts/yotta_logwatch.py scan --path auth.log --min-severity medium

# 调低爆破阈值 / 时间窗
python3 scripts/yotta_logwatch.py scan --path auth.log --max-fail 3 --window 120

# 从标准输入读取（管道）
type auth.log | python scripts/yotta_logwatch.py scan --stdin

# JSON 输出
python3 scripts/yotta_logwatch.py scan --path auth.log --json
```

退出码：**0** = 无命中；**1** = 有命中；**4** = 用法或读取错误。

## 工作流程（AI 智能体执行日志审计时）

1. **确认范围**：明确要分析的日志文件 / 目录与日志类型；只读本地，不做任何外部动作。
2. **读取**：用 `scan --path` 指向文件或目录；目录默认只取日志特征文件（*.log / *.txt / *.out / *.access / *.err / *.audit 或文件名含 auth/access/secure/powershell/syslog/error/system/event）。
3. **检测**：引擎按类型自动嗅探或 `--type` 指定，逐类跑检测规则。
4. **分析**：按严重度（info / low / medium / high / critical）核对命中；`--min-severity` 过滤低价值噪音。
5. **报告**：文本 / JSON / Markdown 三种输出；`--output` 写文件，默认打印。
6. **决策纪律**：只做只读分析并给建议；不联网、不主动扫描、不改动日志；命中只说明「可疑」，需人工核实确认。

## 功能

- **四类日志解析**：auth/secure（sshd / login / sudo…）、Web 访问日志（common/combined）、PowerShell 脚本块日志、Windows 事件日志（Security/System，key=value / wevtutil 文本 / XML 单行导出）；
- **类型自动嗅探**：无需手动指定，按行特征判断类型；也可 `--type` 强制；
- **auth 检测**：失败登录聚合 / 同源爆破 / 时间窗内多账号撞库 / 异常登录（失败后成功）/ root 直登 / sudo 提权与越权尝试；
- **web 检测**：404 洪峰 / 扫描器探测特征 / webshell 上传·访问轨迹 / 路径遍历 / SQL 注入 / 可疑 User-Agent；
- **powershell 检测**：编码命令 / 下载执行 / 反射加载 / AMSI 绕过 / 混淆启发式；
- **winevt 检测**：登录失败聚合（爆破 / 撞库）/ 异常·管理员·RDP 登录 / 账户创建·删除·锁定 / 组成员添加 / 安全日志清空 / 可疑进程创建 / 新服务安装 / 计划任务创建；
- **时间线 + 中文说明**：命中按时间排序，每条含类型、严重度、证据行、中文说明与复核建议；
- **三种输出**：文本 / JSON（stdout 纯净）/ Markdown 报告。

详细的规则与阈值说明见 references/。

## 检测规则一览

| 类别 | 命中类型 | 严重度 | 说明 |
|---|---|---|---|
| auth | brute_force | low~high | 同源多次失败登录（--max-fail 阈值） |
| auth | credential_stuffing | high | 同源尝试多个不同用户名 |
| auth | abnormal_login | high | 同源多次失败后成功登录 |
| auth | root_login | medium | 来源以 root 直登 |
| auth | sudo_escalation / sudo_attempt | medium~high | sudo 提权 / 越权（not in sudoers） |
| web | path_traversal | high | 路径穿越（../ 或编码变体） |
| web | sql_injection | high | SQL 注入特征 |
| web | webshell_upload | critical | webshell 上传 / 访问轨迹 |
| web | suspicious_ua | low | 已知扫描 / 自动化工具 UA |
| web | scanner_signature | medium | 命中多个管理 / 敏感路径 |
| web | flood_404 | medium | 同源 404 洪峰（--404-threshold 阈值） |
| powershell | encoded_command | high | -EncodedCommand / 长 base64 |
| powershell | download_execute | critical | 下载器 + 远程执行 |
| powershell | reflection | medium | .NET / 内存反射加载 |
| powershell | amsi_bypass | critical | AMSI 绕过字符串 |
| powershell | obfuscation | medium | iex / [char] / 拼接等混淆 |
| winevt | brute_force | low~high | 同源多次 4625 登录失败（--max-fail 阈值） |
| winevt | credential_stuffing | high | 同源 4625 尝试多个用户名 |
| winevt | abnormal_login | high | 同源先 4625 失败后 4624 成功 |
| winevt | rdp_logon / admin_logon | medium | 4624 远程桌面（Type 10）/ 管理员登录 |
| winevt | account_created / account_deleted | high | 4720 账户创建 / 4726 账户删除 |
| winevt | account_locked | medium | 4740 账户被锁定 |
| winevt | group_member_add | medium~high | 4732/4728 组成员添加（管理员组 → high） |
| winevt | audit_log_cleared | critical | 1102 安全日志被清空 |
| winevt | suspicious_process | low~critical | 4688 可疑进程创建（LOLBin / 编码命令等） |
| winevt | service_installed / task_created | medium | 7045 新服务 / 4698 计划任务（持久化） |

## 边界（安全红线）

- **只读本地**：不联网、不主动扫描、不修改 / 删除 / 写入任何日志内容；
- **不提供利用**：所有命中只做「可疑提示 + 复核建议」，不提供利用细节；
- **授权**：仅用于已获明确授权 / 自有资产 / CTF 靶场 / 教学环境的安全审计；未经授权分析他人系统数据违反法律，使用者自行承担责任。
- **安装边界**：安装脚本只写用户显式指定的目标（`--agent` / `--dir`）；批量安装到全部已知智能体目录
  必须显式加 `--yes`，不做静默多目录写入；目标若是符号链接一律拒绝。

## 参考文档

- references/auth-log-rules.md — auth 日志检测规则与阈值说明
- references/web-log-rules.md — Web 访问日志检测规则与特征表
- references/powershell-log-rules.md — PowerShell 脚本块检测规则与启发式
- references/windows-event-rules.md — Windows 事件日志检测规则（EventID 语义与阈值）
- references/analysis-spec.md — 元察分析规范（判型 / 字段提取 / 风险判定 / SOP / 输出报告）

## 法律声明

本技能仅用于**已获明确授权**的安全审计（自有资产、授权测试、CTF 靶场、教学环境）。
未经授权分析他人系统数据违反中国《网络安全法》与《刑法》相关条款，使用者自行承担法律责任。
