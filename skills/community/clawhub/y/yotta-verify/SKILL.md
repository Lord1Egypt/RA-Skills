---
name: yotta-verify
slug: yotta-verify
version: 0.3.6
displayName: 元信·装前安全扫描
summary: 装任何技能前的确定性安全扫描：提示注入 + 危险模式 + 完整性检查，输出四档安全裁决。
description: '元信 —— 装任何技能/包前的确定性安全扫描器：prompt injection（提示注入）+ 危险模式 + SKILL.md 完整性 + 权限需求，输出 verdict（SAFE TO INSTALL / INSTALL WITH CAUTION / REVIEW REQUIRED / DO NOT INSTALL）+ audited 徽章。触发：安装/评估任何技能或 npm 包前、给技能做安全验证、生成 audited 徽章、CI 装前闸门；或用户说 装前扫描/验证/audited/安全验证/verify-skill/可信 等。边界：只做确定性静态扫描与报告，不执行被测代码、不联网、不装包、不修复；结论需人工确认，不代替最终决策。'
tags: [装前扫描, 提示注入, 危险模式, 安全裁决, security scan, 安全]
category: it-ops-security
license: MIT
homepage: https://github.com/YottaMeta/yotta-verify
---
# 元信（yotta-verify）

装任何技能 / 包之前的「确定性安全验证」——扫描 prompt injection、危险模式、SKILL.md 完整性
与权限需求，给出一句话 verdict 与可随包发布的 **audited 徽章**：

- **scan**：装前安全扫描（提示注入 + 危险模式 + 技能结构 + 权限需求），输出 verdict。
- **badge**：生成 audited 徽章（本地 SVG + shields.io URL；validate-skill + 元安/元审 verdict + 版本 + 引擎测试数）。
- **report**：生成 SKILL VERIFY REPORT（Markdown / JSON）。
- **gate**：CI 装前闸门（默认阈值 medium，超出即失败）。

元阁安装链路会读取 `skill-manifest.json` 中的 `before_install` 声明：扫描不通过时阻断落位并保留旧版本，证据写入元阁本地审计日志。

零依赖（Python 3.8+ 标准库），Windows + Linux + macOS 通用。危险模式规则与元安
（yotta-security-audit）共用（scripts/verify_rules.py 为同步副本，勿手改）。

## 何时使用

- 从技能市场、GitHub、npm 或任何来源获取技能 / 包后、安装前；
- 评估他人分享的技能是否安全、是否值得安装；
- 给自己的技能包生成 audited 徽章、对外宣传「已验证安全」；
- CI 里给技能仓库加装前扫描闸门。

**Do NOT trigger**：本工具只做确定性静态扫描与报告——不执行被测技能代码、不联网、不装包、
不修复、不做动态分析；最终结论必须由人类确认，不代替安装决策。

## 快速使用

```bash
# 装前扫描一个技能目录 / npm 包目录 / tarball
python3 scripts/yotta_verify.py scan ./some-skill

# JSON + Markdown 报告 + audited 徽章
python3 scripts/yotta_verify.py scan ./some-skill --json --report report.md --badge

# 生成 audited 徽章（可合并元审/元安 verdict 与 validate-skill 结果）
python3 scripts/yotta_verify.py badge ./some-skill --validate-skill pass     --vetter-verdict "SAFE TO INSTALL" --audit-verdict "SAFE TO INSTALL" --tests 52

# CI 闸门：最严重级超过 medium 即失败（exit != 0）
python3 scripts/yotta_verify.py gate ./some-skill --max-severity medium
```

## verdict 判定

| 最高严重级 | verdict | 退出码 |
|---|---|---|
| critical | DO NOT INSTALL | 3 |
| high | INSTALL WITH CAUTION | 2 |
| medium | REVIEW REQUIRED | 1 |
| low/info | SAFE TO INSTALL | 0 |

exit code 与元安 / 元审一致（0 / 1 / 2 / 3 / 4 = 错误）。

## 检测能力（8 检测点威胁捕获模型 + 13 行为项）

0. **威胁捕获模型（8 检测点）**：供应链风险 / 命令执行风险 / 网络请求与数据外传 /
   文件操作与敏感路径访问 / Prompt 注入风险 / 远程脚本下载执行 / 可疑编码·混淆 / 其他安全风险；
   报告按 8 类逐类给 verdict（danger / suspicious / safe / n/a）。

1. **Prompt Injection（提示注入）**：指令覆盖（ignore-previous-instructions 类）、角色伪造、
   隐藏/编码指令（base64 解码命令）、数据外传指令、分隔符逃逸 / 伪系统标签、工具自执行指令、
   越权 / 隐藏意图（don't-tell-the-user 类）、凭据 / 输入采集。详见 references/injection-patterns.md。
2. **危险模式（与元安共用规则，54 → 61）**：下载即执行 / 混淆执行 / 持久化 / 数据外传 / 凭据窃取 /
   网络调用 / 权限提升 / 社会工程 + 新增 **路径穿越（PathTraversal）/ MCP 命令执行（MCPCommandExec）/
   MCP 任意文件读写（MCPFileAccess）**。
2.5 **MCP 工具面（L3）**：识别 MCP server 工具集，追踪「工具参数 → 危险 sink」，
   恶意 MCP（参数流入 spawnSync / execSync / 任意文件读写）判 **DO NOT INSTALL**。
2.6 **数据流（L2）**：argv 注入面 → 子进程 sink 无防护判 medium。
3. **SKILL.md 完整性**：frontmatter 必需字段、name 与目录一致、markdown 围栏平衡、无占位符残留。
4. **权限需求**：脚本引用的网络调用 / 命令执行 / 文件写入 / 敏感文件读取范围（按 8 类归口提示）。

## 报告（双视角综合报告）

- **安全健康度评分**（0-100）；**威胁捕获模型视图**（8 类逐类 verdict）；
- **行为项**（13 项：安装依赖包 / 收集系统信息 / … / 修改 AI 配置）；
- **逐文件 verdict**；**修复建议指南**；**内容 hash**（text / JSON / Markdown 三格式）。

## 授权声明

- 本工具只对**用户有权检查的目标**做静态扫描：自有技能 / 包、已获授权评估的技能与包。
- 扫描只读：不执行被测代码、不联网、不装包、不修改目标文件；输出报告仅供授权范围内的安全评估使用。
- 请勿对无权评估的目标使用；如目标来自他人分享，先确认你有权检查其内容。

## 法律 / 红线声明

- 本工具仅提供**确定性静态安全校验与报告**，不输出攻击 payload、不指导利用、不含双用途内容；
  检测规则与教学文档（references/injection-patterns.md）仅用于装前安全验证与安全教学。
- 使用本工具须遵守所在地法律与相关平台条款；对任何目标的使用责任由使用者自负。
- 与元阁安全家族一致：检测 / 扫描类规则与样例属固有属性，仅用于「让用户敢装」的信任验证，绝不用于攻击。

## 核心功能

- scan / badge / report / gate 全功能开放（确定性静态扫描）。

## 与元安 / 元审的分工

- 元信 = 装前确定性扫描 + 徽章：一句话 verdict，面向「安装决策」与「已验证安全」信任呈现；
- 元审 = 安装前四阶段 checklist 初审（来源 / 代码 / 权限 / 风险）；
- 元安 = 深度扫描：8 类检测器 + 系统安全基线；
- 建议链路：元信 scan（快速 verdict + 徽章）→ 有 medium 及以上转元审四阶段 → high 及以上转元安深度扫描。

## 自扫说明

元信自扫（dogfooding）通过：对自身安装目录扫描无 critical / high。扫描器规则表
（verify_rules.py 等）为签名数据——**按「路径 `scripts/<规则表名>.py` + 内容 SHA-256」双绑定**
跳过，改名或改内容都不再豁免（v0.3.2 起）；`test_*.py` 只在持有已发布签名数据的自家包里跳过，
非自家包同名文件照常扫描，发布包本身用 `!scripts/test_*.py` 排除测试；报告中的 URL 类 low 提示
属预期（shields.io 链接）。

## 参考文档

- references/injection-patterns.md — 提示注入检测模式说明（8 类）
- references/verify-report-template.md — SKILL VERIFY REPORT 模板
- references/badges.md — audited 徽章说明（内容 / 用法 / 嵌入 README）
