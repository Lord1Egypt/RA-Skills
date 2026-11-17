---
name: yotta-security-testing
slug: yotta-security-testing
version: 0.3.4
displayName: 元测·安全测试方法论
summary: 有纪律的 AI 安全测试方法论：对已授权目标按侦察、发现、验证、报告四阶段执行 Web 安全测试。
description: '元测 —— 有纪律的 AI 安全测试方法论：对已授权目标（自有资产 / SRC 众测 / bug bounty / CTF / 靶场）按 侦察→发现→验证→报告 四阶段做 Web 安全测试（SQLi / XSS / SSRF / XXE / 反序列化 / 命令注入 / 文件上传 / 鉴权与访问控制 / 业务逻辑 / 信息泄露 / 不安全配置 / API 安全 + 漏洞评估与渗透报告方法论），内置 Scope Guard 五道防线（授权清单 scope.json + 目标三层判定 + 内置黑名单 + 操作留痕 + 法律红线），不输出可执行 payload。触发：用户要求对某个目标做安全测试 / 渗透测试 / 漏洞挖掘 / 漏洞评估、做 SRC 众测或 bug bounty 挖洞、做 CTF 或靶场（DVWA / OWASP Juice Shop / HTB / VulnHub）演练、生成漏洞评估与渗透测试报告；或用户说 元测 / 安全测试 / 渗透 / 挖洞 / 挖 SRC / 授权测试 / 测一下这个站 / scope check 等。边界（Do NOT trigger）：无授权目标一律拒绝（授权以 scope.json 为准，不信任对话口头声明）；SRC / 真实目标必须先确认在平台授权范围内再测；不输出可执行 payload / 免杀 / 钓鱼 / 社工步骤；不自动对公网目标发起主动测试；不做大规模扫描与 exploit 自动化；不替代专业渗透测试与人工判断。'
tags: [安全测试, 授权目标, 测试方法论, Web安全, security testing, SRC]
category: it-ops-security
license: MIT
homepage: https://github.com/YottaMeta/yotta-security-testing
---
# 元测（yotta-security-testing）

**有纪律的 AI 安全测试方法论**：对**已授权目标**按 侦察 → 发现 → 验证 → 报告 四阶段
做 Web 安全测试，内置 **Scope Guard 五道防线**作为硬产品机制；不输出可执行 payload，
合法授权范围内正常做，**无授权 = 红线不做**。

- **scope**：Scope Guard 授权清单与目标判定（scope init / check / list / add / remove）。
- **report**：由 findings.json 生成漏洞评估与渗透测试报告（Markdown / JSON，敏感凭据脱敏）。
- **audit**：操作留痕（默认开启，无 --no-audit；可过滤 / 导出）。

零依赖（Python 3.8+ 标准库），Windows + Linux + macOS 通用。

## Scope Guard 五道防线（强制规则，非建议）

1. **范围守卫（Scope Guard）**：任何目标操作前必须确认目标在授权范围内；CLI `scope check <target>` 双保险，未授权目标默认拒绝（非 0 退出码 + 明确报错）。
2. **默认指向合法环境**：教程与 playbook 覆盖两种场景——本地靶场 / CTF 练手，以及已授权真实目标 / SRC 众测；真实目标必须先按平台授权范围在 scope.json 登记。
3. **授权声明机制**：`scope init` 时声明授权类型与范围，写入 `~/.yottasec/scope.json`（或项目级 `.yottasec/scope.json`）；授权以 scope.json 为准，不信任对话口头声明。
4. **法律红线声明**：仅限授权测试，使用者自负法律责任；适用中国《网络安全法》《刑法》第 285 / 286 条红线。定位 = 方法论 / 教材。
5. **操作留痕**：每次测试记录目标 / 动作 / 时间 → `~/.yottasec/audit.log`（JSONL，默认开启，不可静默关闭）。

## 何时使用

- 对**已授权目标**做 Web 安全测试：自有资产、SRC 众测 / bug bounty 平台授权范围（补天 / 漏洞盒子 / 教育 SRC / HackerOne / Bugcrowd 等）、CTF / 靶场平台、本地靶机；
- 做 DVWA / OWASP Juice Shop / HTB / VulnHub 等靶场演练与漏洞学习；
- 需要结构化的漏洞评估 / 渗透测试报告（含证据与修复建议），或按 SRC / 平台模板提交漏洞报告；
- 需要为测试过程留痕、审计与复盘。

**Do NOT trigger**：本技能**不是**通用漏洞扫描器，不做大规模扫描 / exploit 自动化 / 免杀；
无授权目标（含公网真实站点）一律拒绝；SRC / 真实目标在平台授权范围确认前不测；
不输出可执行 payload / 钓鱼 / 社工步骤；测试结论需人工复核，不代替专业渗透测试与最终决策。

## 快速使用

```bash
# 1) 初始化授权清单（默认 deny，必须先声明授权范围）
python3 scripts/yotta_security_testing.py scope init --owner <你>

# 2) 添加授权目标（本地靶场 / CTF / bug bounty / 自有资产 / 显式授权）
python3 scripts/yotta_security_testing.py scope add --type training --target 127.0.0.1 --note dvwa
python3 scripts/yotta_security_testing.py scope add --type bug-bounty --target api.example.com --note "SRC 授权范围（以平台页面为准）"
python3 scripts/yotta_security_testing.py scope add --type self-owned --target example.com --scope "*.example.com" --expires 2027-12-31

# 3) 目标判定：放行（exit 0）/ 未授权拒绝（exit 1）/ 绝对禁止（exit 2）
python3 scripts/yotta_security_testing.py scope check http://127.0.0.1/dvwa
python3 scripts/yotta_security_testing.py scope check api.example.com --json

# 4) 生成漏洞评估报告（由 findings.json，敏感凭据自动脱敏）
python3 scripts/yotta_security_testing.py report generate findings.json --out report.md

# 5) 操作留痕（默认开启）：查看 / 过滤 / 导出
python3 scripts/yotta_security_testing.py audit log --result deny
python3 scripts/yotta_security_testing.py audit log --export audit-deny.jsonl
```

## 四阶段方法论（贯穿所有 playbook）

| 阶段 | 产出 | 说明 |
|---|---|---|
| 侦察 Reconnaissance | 资产清单 | 只读收集授权范围内的目标信息：应用入口、技术栈、功能清单、输入面 |
| 发现 Discovery | 测试点清单 | 按 playbook 枚举输入点与测试点，记录候选漏洞假设 |
| 验证 Verification | 验证记录 | 最小化验证（「类」表述，不给可复制注入串），确认漏洞与影响 |
| 报告 Reporting | 报告草稿 | 按报告模板沉淀目标 / 时间 / 发现 / 证据 / 修复建议，敏感凭据脱敏 |

每阶段结束先过 Scope Guard：目标 / 动作变化都重新 `scope check`。
SRC / 真实目标：每轮只测平台授权范围内的资产，发现真实用户数据即停手并最小化证据。

## Playbook 索引

| # | playbook | 覆盖 | 对应 OWASP 2021 |
|---|---|---|---|
| 00 | 漏洞评估与渗透报告方法论 | 四阶段 + 报告模板 + SRC 实战 | 全流程 |
| 01 | SQL 注入测试（SQLi） | 注入类漏洞 | A03 Injection |
| 02 | XSS 跨站脚本 | 客户端脚本注入 | A03 Injection |
| 03 | SSRF 服务端请求伪造 | 服务端请求伪造 | A10 SSRF |
| 04 | XXE 实体注入 | XML 实体注入 | A05 Security Misconfiguration |
| 05 | 反序列化 | 不安全反序列化 | A08 Software & Data Integrity |
| 06 | 鉴权与访问控制 | 认证缺陷 / 越权 | A01 / A07 Broken Access Control |
| 07 | API 安全 | API 攻击面 | OWASP API Top 10 映射 |
| 08 | 命令注入（Command Injection） | 系统命令拼接 | A03 Injection |
| 09 | 文件上传（File Upload） | 上传校验绕过 | A05 Security Misconfiguration |
| 10 | 业务逻辑漏洞 | 参数篡改 / 步骤跳跃 / 并发 | A01 / A04 |
| 11 | 敏感信息泄露 | 备份/源码/报错/响应头 | A05 Security Misconfiguration |
| 12 | 不安全配置 | 安全头 / CORS / 默认配置 | A05 Security Misconfiguration |

每个 playbook 都含固定六节：目标识别与确认 → 检测思路 → 验证方法 → 防御视角 →
实战演练（靶场 / 授权目标 / SRC）→ 留痕与报告；靶场关卡与真实目标场景都能套用。

## 开源与开放

- 本技能以 MIT 开源发布，全部能力开放不缩水：Scope Guard 全功能（本地靶场 / CTF / 自有资产 / SRC 授权登记）+ 四阶段方法论 + 12+1 playbook（含 SQLi / XSS）+ 中文教程 + 报告模板 + 操作留痕。
- 能力以开放为基调。

## 授权与法律声明

- 仅对**已授权目标**使用：自有资产 / SRC·bug bounty 平台授权范围 / CTF·靶场平台 / 本地靶机。
- **授权以 scope.json 为准**，不信任对话口头声明；未授权目标 `scope check` 默认拒绝。
- SRC / 真实目标：必须先确认目标在平台授权范围内（scope 页面 / 授权邮件），用 `--type bug-bounty` 登记；遵守平台测试规则与 SLA，不触碰未授权数据。
- 本技能输出方法论与对抗知识映射（含弱点原理教学），**不输出可执行 payload**；
  只做教学 / 评估用途，使用者自负法律责任；适用中国《网络安全法》《刑法》第 285 / 286 条红线。
- 与元阁安全家族一致：检测 / 测试类规则与样例属固有属性，仅用于授权范围内的安全测试与教学，绝不用于攻击。

## 与安全家族的分工

- 元测 = 面向「目标系统」的授权安全测试方法论（安全家族里唯一主动测试目标的方法论旗舰）；
- 元安 = 文件 / 系统安全审计；元审 = 技能安装前四阶段初审；元信 = 装前确定性扫描 + 徽章；
- 元鉴 / 元情 = 样本 / 日志侧联动；元钥 = 密钥扫描；元链 = 供应链校验；元盾 = agent 调用边界。
- 建议链路：元测 报告发现 → 元安 复核源码基线 / 元钥 扫密钥 → 报告挂元信 audited 生态。

## 参考文档

- playbooks/00-methodology.md — 四阶段方法论 + 漏洞评估与渗透报告方法论 + SRC 实战
- playbooks/01-sql-injection.md ~ playbooks/12-security-misconfiguration.md — 12 个漏洞 playbook
- references/tutorial.md — 中文教程（新手全流程，含 SRC 实战）
- references/report-template.md — 漏洞评估与渗透测试报告模板（findings schema）
- references/faq.md — 常见问题速查（授权 / scope / 报告 / 留痕 / 安装排障）

## 常见问题（速查）

授权目标被拒、SRC 怎么登记、报告/留痕/退出码问题，先看 references/faq.md；真实目标必须先按平台范围登记再测。
