---
name: yotta-verify-mcp
slug: yotta-verify-mcp
version: 0.4.7
displayName: 元信·装前扫描服务
summary: 把装前安全扫描做成工具服务：扫描技能、生成审计徽章、CI 闸门、报告输出，本地离线。
description: '元信MCP（yotta-verify-mcp）—— 把元信（yotta-verify）装前安全扫描暴露为 stdio MCP server，提供 scan_skill（目录/包 → verdict+发现）、generate_badge（audited 徽章）、gate_check（CI 闸门）、get_report（JSON/Markdown 双视角综合报告）四个 MCP 工具。触发：给 MCP 客户端配置元信MCP、把装前信任扫描接入智能体/工作流、调用上列 MCP 工具做扫描；或用户说 MCP元信/元信MCP/trust-mcp/scan-mcp 等。边界：本地离线静态扫描，不上传被测内容、不执行被测代码、不联网；结论需人工确认。MCP 配置与全局/永久记忆写入均为可选，必须先获得用户明确同意；未获同意前不写任何文件，可直接降级 CLI。'
tags: [装前扫描, MCP, 安全闸门, 审计徽章, security scan, 工具服务]
category: it-ops-security
license: MIT
homepage: https://github.com/YottaMeta/yotta-verify-mcp
---
# 元信MCP（yotta-verify-mcp）

把元信（yotta-verify）的装前安全扫描做成 **stdio MCP server**——在安装技能 / 插件 / MCP 服务器之前，
先拿到确定性 verdict。零依赖（Python 3.8+ 标准库），复用 `yotta_verify.py` 内核与 `verify_rules.py`
规则表（单源），本地离线静态扫描。

**基于 MCP 最新协议 2026-07-28（无状态时代；向后兼容 2025-11-25 及更早握手客户端）。**

## 使用须知（先做这一步）

本技能按需触发，不要求修改宿主配置，也不要求把指令写入全局/永久记忆。

若用户希望配置 MCP server 或添加跨会话提醒，AI 必须先展示目标文件路径、完整写入内容与影响，
并获得用户明确同意；未获同意前不写任何文件。用户拒绝时不写，直接使用 CLI，功能不受影响。

## MCP 客户端接入（可选；需用户明确同意）

写客户端配置前必须先获得用户明确同意。AI 只能提供配置建议或代写草稿；是否写入由用户决定。

1. 检查当前 MCP 客户端的 `mcpServers` 是否已有 `yotta-verify-mcp` 条目；已有则直接使用。
2. 若没有，先向用户展示目标配置文件路径、将写入的完整 JSON、写入后的影响，以及两种可选方式：
   - **方式 A · 本地 Python 脚本（完整安装 / 离线可用）**
     ```json
     {
       "mcpServers": {
         "yotta-verify-mcp": {
           "command": "python",
           "args": ["<技能目录>/scripts/yotta_verify_mcp.py"]
         }
       }
     }
     ```
     > `<技能目录>` = 本技能实际安装目录，**不要写死盘符路径**；Windows 用 `python`，Linux/macOS 用 `python3`。
   - **方式 B · npm**
     ```json
     {
       "mcpServers": {
         "yotta-verify-mcp": {
           "command": "npx",
           "args": ["-y", "@yottameta/yotta-verify-mcp"]
         }
       }
     }
     ```
3. 用户明确同意后，才可写入配置；用户拒绝则不写。用户也可以自行复制上面的 JSON 手动粘贴。
4. 修改 `mcpServers` 后，多数客户端需要重启 / 重载一次 MCP server 才生效；加载后应看到四个工具。
5. 未配置 MCP 或用户拒绝配置时，直接使用 CLI 扫描，功能不受影响：
   `python <技能目录>/scripts/yotta_verify_mcp.py` 或 `npx -y @yottameta/yotta-verify-mcp`。

## 跨会话提醒（可选；需用户明确同意）

如果用户希望后续会话也记得优先做装前扫描，可以把下面的建议文本加入客户端的全局/永久记忆。
这是可选步骤，不是使用本技能的前提；写入前必须先获得用户明确同意，未获同意前不写任何文件。

建议文本（经用户确认后可由 AI 写入，或由用户自行粘贴）：

```markdown
# 装前扫描提醒（来源：yotta-verify-mcp · 元信MCP）
安装或首次使用技能 / 插件 / MCP server 前，建议先调用元信MCP 或其 CLI 做装前安全扫描，并由用户确认扫描结论。
```

执行顺序：

1. 展示目标文件路径、上述完整文本与写入后的影响。
2. 获得用户明确同意后再写入；用户拒绝则不写。
3. 写入后回读确认；目标文件已有同段内容则跳过，不重复堆叠。
4. 拒绝写入或文件不可写时，直接使用 CLI，功能不受影响。

## 按需使用（用户确认后执行）

- 用户要求安装或评估技能 / 插件 / MCP server 时，AI 先建议执行装前扫描；经用户确认后调用
  `scan_skill` 或 `gate_check`，或直接使用 CLI。
- 扫描完成后本技能不主动参与后续会话；是否保留 MCP 配置由用户决定。
- 所有“该装 / 不该装”的判断都必须说明这是扫描结论，最终由用户确认。

## 何时使用

- 用户要在 MCP 客户端里配置「元信 MCP」server，或问「怎么接元信 MCP」；
- 在智能体 / 工作流里调用 `scan_skill` / `generate_badge` / `gate_check` / `get_report`
  对某个技能、目录或 npm 包做装前信任扫描；
- 用户说 **MCP元信 / 元信MCP / trust-mcp / scan-mcp / 装前扫描** 等。

**Do NOT trigger**：只做确定性静态扫描与报告——不执行被测代码、扫描中不联网、不装包、
不修复、不做动态分析；目录扫描完全离线，npm 包扫描仅下载公开包到临时目录；最终结论由人类确认。

## 四个 MCP 工具

| 工具 | 说明 |
|---|---|
| `scan_skill` | 只读参数 `target`（目录 / .tgz / npm 包）。返回 verdict + 严重级统计 + 发现 |
| `generate_badge` | 生成 audited 徽章（本地 SVG + shields.io URL）。可带 `target` 自动 scan 取 verdict、或直接给 `verdict`，并可并入 `validate/vetter/audit/version/tests` |
| `gate_check` | CI 闸门。`target` + `max_severity`（默认 medium），返回 `pass/verdict/worst/code` |
| `get_report` | 生成报告。`target` + `format`（json/markdown）、可写 `out` |

## 使用流程

1. **配置（可选）**：按「MCP 客户端接入」展示目标文件与完整配置，获得用户明确同意后再写入；
   用户拒绝则不写，直接使用 CLI。
2. **确认**：用户确认扫描目标后调用 `scan_skill`，或直接 `gate_check` / `get_report`。
3. **解读**：verdict（SAFE TO INSTALL / INSTALL WITH CAUTION / REVIEW REQUIRED / DO NOT INSTALL）
   是确定性静态结论；发现里 low/info（如 URL 类）属预期，需人工复核是否真风险。
4. **收尾自检**：给用户「一句话 verdict + 是否建议安装」；涉及「该装 / 不该装」的决策必须说明
   「这是扫描结论，请自行确认」。

## 边界与提示

- `generate_badge` 的 `version` 段**默认取扫描引擎（yotta-verify）版本**（如 0.1.1），不是 MCP 包版本；
  想显示别的版本传 `version`。
- 目录扫描完全离线；npm 包扫描仅下载公开包（临时目录，扫后删除），不上传被测内容。
- 只扫描用户**有权评估**的目标。

## 范围声明（Scope Guard）

元信 MCP 的作用域是**装前信任验证**：在安装 / 使用一个技能、插件或 MCP 服务器之前，
给出确定性静态扫描结论。它**不**做运行时沙箱、**不**做动态分析、**不**做渗透测试、
**不**修复目标——超出装前静态验证范围的事不做。

## 授权声明

- 本工具只对**用户有权检查的目标**做静态扫描：自有技能 / 包、已获授权评估的技能与包。
- 扫描只读：不执行被测代码、扫描中不联网、不装包、不修改目标文件；输出报告仅供授权范围内的安全评估使用。
- 请勿对无权评估的目标使用；如目标来自他人分享，先确认你有权检查其内容。

## 法律 / 红线声明

- 本工具仅提供**确定性静态安全校验与报告**，不输出攻击 payload、不指导利用、不含双用途内容；
  检测规则与教学文档仅用于装前安全验证与安全教学。
- 使用本工具须遵守所在地法律与相关平台条款；对任何目标的使用责任由使用者自负。
- 与元阁安全家族一致：检测 / 扫描类规则与样例属固有属性，仅用于「让用户敢装」的信任验证，绝不用于攻击。

## 渐进披露

- 细节放 `references/`，按需读取，不要每次全读。
- `references/trust-checklist.md` — MCP 服务器 / 插件装前信任清单（来源可核 / 装前扫描 /
  权限声明核对 / 最低权限 / 审计留痕 / 定期复查）。
