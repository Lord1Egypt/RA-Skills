---
name: yotta-security-audit
slug: yotta-security-audit
version: 0.3.3
displayName: 元安·技能安全审计
summary: 检测 AI 技能恶意模式、系统安全基线与学生数据隐私风险（教育版）：15 条学生数据规则 + 报告脱敏，纯只读、零依赖。
description: '元安 —— 检测 AI 技能中的恶意模式（13 类检测器）、系统安全基线（Windows/Linux）与学生数据隐私风险（教育版，15 条规则），纯只读、零依赖、有纪律。触发：用户提到 安全审计 / 技能安全检查 / 恶意检测 / 供应链安全 / 系统安全基线 / 学生数据 / 学生个人信息 / 隐私扫描 / 校园数据合规 / scan skills / supply chain / malicious skill / 扫描技能 等。边界：本工具只检测与报告，绝不执行修复、删除或查杀动作；学生数据扫描不回显原文，不提供法律或合规结论。'
tags: [安全审计, 恶意检测, 学生数据隐私, 供应链安全, security audit, 基线检查]
category: it-ops-security
license: MIT
homepage: https://github.com/YottaMeta/yotta-security-audit
---
# 元安（yotta-security-audit）

YottaMeta 自有安全扫描引擎，三种只读模式：

- **技能模式**（--target skill，默认）：扫描 AI 技能目录中的恶意模式，13 类检测器覆盖后门、凭据窃取、数据外传、持久化、供应链安装钩子等。
- **系统模式**（--target system）：系统安全基线扫描，Windows / Linux 平台感知，只读不改系统。
- **教育版**（--target edu）：学生数据隐私风险扫描，面向班级资料目录 / 成绩表 / 名单等文件，输出类别、位置、计数与脱敏样例，不回显原文。

纯 Python 3.8+ 标准库实现，零依赖；Windows + Linux 通用。

## 何时使用

- 安装任何新技能前，先扫描其目录；
- 定期扫描本机已安装的全部技能（自动发现 17 类智能体技能目录）；
- 怀疑技能存在恶意行为、需要审计时；
- 检查系统安全基线（启动项、计划任务、服务、防火墙、共享、权限点等）；
- 盘点班级资料目录里的学生个人信息（身份证号 / 手机号 / 住址 / 健康与资助信息等）与出本机风险；
- 对外分享成绩、名单、评语前，先确认文件里有没有不该出现的字段。

**Do NOT trigger**：本工具只读检测。发现风险后应向用户报告并给出建议，不得自行删除、隔离或修复；教育版不做学生年龄或身份推断，不给出法律 / 合规结论。

## 快速使用

```bash
# 扫描所有已发现的技能（17 类智能体目录）
python3 scripts/yotta_audit.py --target skill

# 扫描单个技能目录
python3 scripts/yotta_audit.py --path ./some-skill

# 系统安全基线（当前平台）
python3 scripts/yotta_audit.py --target system --platform auto

# JSON 输出 + 生成 Markdown 报告
python3 scripts/yotta_audit.py --path ./some-skill --json --report report.md

# 只报告 high 及以上
python3 scripts/yotta_audit.py --path ./some-skill --severity high

# 教育版：盘点一个班级资料目录
python3 scripts/yotta_audit.py --target edu --path ./班级资料

# 教育版：单文件 + JSON + Markdown 报告（报告不得写入被扫描目录）
python3 scripts/yotta_audit.py --target edu --path ./成绩表.xlsx --json --report ./edu-report.md

# 教育版：学校自备词表 / 规则包
python3 scripts/yotta_audit.py --target edu --path ./校车名单.csv --edu-rules ./school-rules.json
```

Windows 下同样用 python 运行；控制台编码已加固（GBK 环境不崩）。

## 工作流程（AI 智能体执行审计时）

1. **确定范围**：用户指定目录用 --path；未指定则自动发现全部技能目录（教育版必须显式 --path，不自动发现）。
2. **运行扫描**：执行上述命令，先看文本报告，必要时 --json 拿结构化结果。
3. **分析结果**：按严重级排序逐条核对；区分「真风险」与「需结合上下文的提示」（NetworkCall / 高熵 / URL 等多为上下文相关）。
4. **报告用户**：给出 发现数（按级别）、关键发现的位置与描述、建议动作。
5. **决策纪律**：发现高风险时，建议用户先隔离/停止使用该技能，再人工复核；工具本身不做任何变更。
6. **教育版纪律**：报告只给类别、位置、计数与脱敏样例；需要条款级判断时用元规（yotta-compliance），需要处置时由用户决定，工具不移动、不删除、不加密任何文件。

## 13 类检测器

| 检测器 | 关注点 | 默认级别 |
|---|---|---|
| DownloadExec | 下载后通过管道或落地文件交给 shell 执行 | critical |
| Obfuscation | 动态求值、编码字符串构造、base64 解码后执行 | high |
| Persistence | 定时任务、启动代理/守护、shell 配置、注册表启动项写入 | high |
| Exfiltration | 读取敏感文件后外传、打包上传 | high |
| CredentialTheft | SSH/云凭据/浏览器数据/钥匙串访问 | critical |
| NetworkCall | 反向连接、原始套接字、HTTP 客户端（多为上下文相关） | medium |
| PrivilegeEscalation | 权限位修改、setuid、加入管理员组 | high |
| SocialEngineering | 社会工程话术命名（文件名） | medium |
| Base64 | 超长 base64 编码串（解码含敏感关键字则升级） | medium→high |
| IOCMatch | 已知恶意 IP/域名/URL 模式/文件哈希 | critical |
| PostInstallHook | 安装期生命周期脚本（下载/执行为 critical） | high→critical |
| HiddenChar | 零宽字符与双向覆盖字符 | medium |
| Entropy | 高熵编码串（疑似混淆/加密载荷） | medium |

规则表位于 scripts/audit_rules.py（签名数据文件，自扫豁免），可用 --ioc-db 传入自有威胁情报。

## 教育版：学生数据隐私规则（15 条）

规则包位于 scripts/student_data_rules.json（版本化 JSON，只作为数据读取、不执行表达式），可用 --edu-rules 换成学校自备词表：

| 规则 | 关注点 | 默认级别 |
|---|---|---|
| EDU-ID-001 | 身份证号明文（18 位 + 校验位） | critical |
| EDU-ID-002 | 手机号 | high |
| EDU-ID-003 | 邮箱 | medium |
| EDU-ID-004 | 学籍号 / 考生号字段（字段驱动） | medium |
| EDU-QI-001 | 姓名 + 成绩组合 | high |
| EDU-QI-002 | 出生日期 | high |
| EDU-QI-003 | 家庭住址 | high |
| EDU-QI-004 | 家长联系方式 | high |
| EDU-SA-001 | 健康与身心状况 | critical |
| EDU-SA-002 | 资助与家庭境况 | critical |
| EDU-SA-003 | 生物识别信息 | critical |
| EDU-SA-004 | 显式未成年人标记 | critical |
| EDU-HR-001 | 出本机路径（云同步 / 网盘 / 即时通讯目录） | high |
| EDU-HR-002 | 文件名疑似含姓名且与成绩 / 评语相关 | high |
| EDU-HR-003 | AI 工具 / 临时目录 | medium |

判定与隐私约束：

- 解析范围：CSV / TSV / TXT / MD / JSON 等文本，以及 xlsx / docx（标准库只读轻解析）；PDF、图片、扫描件、旧版 Office、压缩包不解析（不做 OCR），在报告中计入「未解析 / 跳过」；
- 判定以字段名（表头）为主、内容正则为辅；身份证号必须通过校验位；学籍号只做字段驱动的形态提示；
- 报告固定脱敏：身份证 / 学籍号 / 手机号保留末 4 位，姓名保留姓，地址保留前 3 个字符，邮箱保留首字符与域名；**不提供明文回显选项**；
- 不做学生年龄或身份推断、不做跨文件个体关联、不联网、不缓存原文；只读打开，绝不修改被扫描文件；
- 报告输出路径不得位于被扫描目录内，也不得与输入文件相同；
- 级别是风险提示分级，不是法律定性；需要条款级判断时使用元规（yotta-compliance）。

## exit code 语义（三技能统一）

| 值 | 含义 |
|---|---|
| 0 | 干净 / 仅有 low 提示 |
| 1 | 存在 medium |
| 2 | 存在 high |
| 3 | 存在 critical |
| 4 | 扫描器自身错误（参数错误/致命异常） |

## 安全边界（Scope Guard）

- **只读**：所有检测均为读取操作；系统模式只运行只读命令（注册表查询、任务枚举等），绝无写入/删除。
- **授权与法律**：仅允许对已获授权的目标进行检测（自己的系统、自己将要安装的技能、明确授权测试的目标）。未经授权扫描他人系统违反《网络安全法》与《刑法》285/286 条，使用者自行承担法律责任。
- **报告脱敏**：默认不输出私钥内容、环境变量值、完整凭据，只给路径、模式与建议。
- **学生数据**：教育版只读、零网络、不缓存原文；报告一律脱敏且不提供明文回显；不做身份与年龄推断，不做跨文件个体关联；处置动作（移动、删除、加密、分发）由用户决定。
- **自扫**：扫描器可扫描自身而不产生中高危误报（签名规则数据文件自动豁免，--include-self 强制包含）。

## 参考文档

- references/threat-patterns.md — 恶意技能攻击模式详解
- references/remediation-guide.md — 发现风险后的处置建议
- references/system-baseline.md — 系统基线检查项说明
- references/student-data-scan.md — 教育版规则、脱敏口径与使用边界
