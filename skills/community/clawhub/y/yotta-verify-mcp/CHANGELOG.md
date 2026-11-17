# Changelog

## v0.4.7 (2026-11-05)

- 修复 PRI-001 特殊权限位正则误报；刷新家族规则表摘要；发布包排除测试文件。
- 发布门禁批次：发布工作流在 `npm publish` 前执行版本/发布面检查与 `npm test`；测试版本断言改为从 `package.json` 读取；补齐测试脚本。
- 打包与文档：发布包内容、CHANGELOG / README 与交付说明对齐；规则摘要与注册清单同步。

# 更新日志

## v0.4.6 (2026-11-01)

- 安装器 containment：目标根 / 嵌套链接 fail-closed；受管 Hub 链接解析真实目标；精简安装器同口径。

## v0.4.5 (2026-10-01)

- 安装器卫生批次：`bin/install.js` / `install.sh` 统一（未知参数报错 exit 2、`--help` / `--version`、残留清理白名单、嵌套载荷保留）；由模板单一真源渲染，接入漂移门禁。

## v0.4.4 (2026-09-25)

安全修复：与元信引擎同步（可执行载荷 fail-closed + tarball 解包上限）+ 安装器加固。

- 内置的 yotta-verify 引擎副本同步到 v0.4.4：新增 `STR-009`（不可静态分析的可执行 / 二进制载荷不再静默跳过）、tarball 解包成员数 / 单成员 / 总量上限。
- 安装器加固：拒绝对符号链接目标写入、不做整目录删除。
- MCP server 版本、server.json、skill-manifest 同步 0.4.4。

## v0.4.3 (2026-09-19)

**同步扫描内核安全修复（与元信 0.3.2 同源）**：

- 内嵌扫描器同步「签名数据豁免」收紧：规则表跳过改为「路径 `scripts/<规则表名>.py` + 内容
  SHA-256（CRLF 归一化）」双绑定；未验证的同名文件照常扫描。
- `is_detector_skill()` 改由摘要绑定判定，放同名标记文件不再把整包文档命中降级为 info。
- `test_*.py` 跳过只对持有已发布签名数据的自家包生效。
- 校验：`scripts/test_yotta_verify_mcp.py` 57/57；`tools/check_rule_digests.py` 两处副本摘要一致。

## v0.4.2 (2026-09-14)

**STR-004 误报修复（与元信同源）**：

- 同步扫描内核的 name hint 语义：npm tarball 与解压后的 `package/` 根目录从根 `package.json` 的 `name` 推导期望 slug，不再使用临时目录名或压缩包文件名。
- MCP `scan_skill` 对本地 tarball、解压包根与 npm 包名路径统一使用该语义；真实安装目录错名仍保留 STR-004 medium。
- 检测型技能的文档降级不再吞掉 `Structure` 类发现，真实错目录名仍保留 STR-004 medium。
- 新增回归：`package/`、npm tarball、真实错目录名。
- 安全加固：同步内核的 tarball 解压拒绝符号链接、硬链接、设备与 FIFO 成员，Python 3.12+ 叠加官方 `data` 过滤器；新增两组链接成员回归。

## v0.4.1 (2026-09-14)

**授权边界整改**：

- `SKILL.md` / README：MCP 配置与全局/永久记忆写入改为可选，且必须先获得用户明确同意；拒绝时不写，直接降级 CLI，功能不受影响。
- 删除「自动改配置 / 强制写记忆」表述，改为展示目标文件、完整内容与影响后等待用户确认。
- 新增 `test/docs-consent.test.js` 与 `test/version-consistency.test.js`：锁定授权边界文档契约，并要求 CLI `--version`、`package.json`、`SKILL.md` 版本一致。
- 修复启动器 `--version`：不再透传给同源扫描引擎导致返回引擎版本，改为直接输出 MCP 包版本。
- 根仓库 `preflight-publish.py` 补充常驻授权 / 静默写入变体扫描，防止同类漏报。

## v0.4.0 (2026-09-13)

**P0-6 全家族铺开**：

- 新增 `skill-manifest.json`，声明 `before_install` / `scan_skill` / `fallback: wrapper`。
- 强制技能覆盖检查要求包内 manifest 与至少一项 hook 声明。

## v0.3.0 (2026-09-06)

- **MCP 协议对齐最新版 2026-07-28（无状态时代）**：升级 dual-era——modern 直连（server/discover 免握手、逐请求 _meta 版本声明、resultType、-32022 版本错误）服务新客户端；legacy（initialize 握手，protocolVersion 2025-11-25）兼容旧客户端，旧形状响应零惊扰。
- 对外标注：SKILL.md 写明「基于 MCP 最新协议 2026-07-28（向后兼容 2025-11-25 及更早握手）」。
- 测试：新增 modern 用例 6 项，全套件 49/49。

## v0.2.3 (2026-08-30)

- 为官方 MCP Registry 发布新增 package.json `mcpName` 字段（io.github.YottaMeta/yotta-verify-mcp），版本四件对齐 0.2.3。

## v0.2.2 (2026-08-30)

- 措辞规范：正文不再写版本号、统一对外表述；与元信 yotta-verify 同步内核（含双视角综合报告）。

## v0.2.0 (2026-08-30)

安全家族检测能力增强（与元信 yotta-verify 同源）：

- 内核升级：扫描结果现按**8 检测点威胁捕获模型**逐类 verdict + **13 行为项** +
  **安全健康度评分（0-100）** + 逐文件 verdict + 修复建议指南 + 内容 hash（get_report 三格式）。
- **MCP 工具面检测（L3）**：对目标 MCP server 识别工具集、追踪「工具参数 → 危险 sink」
  （spawnSync / execSync / 任意文件读写），恶意 MCP 判 DO NOT INSTALL。
- 新增路径穿越（PathTraversal）/ MCP 命令执行（MCPCommandExec）/ MCP 任意文件读写（MCPFileAccess）检测器
  （规则 54 → 61）。
- 发布包排除测试文件；测试 32 / 32 全绿。

## v0.1.4 (2026-08-29)

- SKILL.md「写入永久记忆」进一步写死**写入内容**：给出必须「逐字原样写入」永久记忆文件的一整段正文（含标题「装前必扫护栏」+ 一句护栏），并明确挂到写入步骤里；不写永久记忆 = 本技能未生效、永远不会跨会话按需自动调用。frontmatter description 已含显式指令。



- SKILL.md「写入永久记忆」措辞强化为**强制执行步骤**：明确「必须把『装前必扫』护栏写入客户端的永久记忆文件（AGENTS.md / 全局记忆），写入后回读核对；永久记忆不可写时显式报告未完成项」。frontmatter description 补显式指令，AI 首次使用本技能时即能看到并执行。



- SKILL.md 新增「写入永久记忆（按需自动调用的保障，必须做）」显式指令：AI 首次使用本技能时必须把「装前必扫（yotta-verify-mcp）」护栏写入客户端永久记忆（AGENTS.md / 全局记忆），确保按需注入跨会话持续生效。

## v0.1.1 (2026-08-29)

- AI 自动接入（MCP 配置，AI 负责）：安装后由 AI 自动写入 `mcpServers`（本地 Python 脚本或 npx 二选一，AI 自选），用户无需手动配置；本地路径用 `<技能目录>/scripts/yotta_verify_mcp.py` 占位、不写死盘符；客户端未暴露 MCP 工具时自动降级 CLI 扫描（verdict 一致）。
- 按需自动调用：安装 / 首次使用某技能、插件、MCP server 前自动调用 scan_skill / gate_check 做装前扫描；完成后不常驻、不卸载。
- README：把 `mcpServers` 两段配置移入 SKILL.md，README 改为指引。

## v0.1.0 (2026-08-29)

初始发布：

- 定位：元信 MCP server —— 把元信（yotta-verify）装前安全扫描暴露为 stdio MCP 工具
  （scan_skill / generate_badge / gate_check / get_report），补 MCP / Agent Plugins 生态的
  「装前信任 / 校验 / 治理」缺口（市场主线 M2 全渠道分发一环）。
- 引擎：零依赖（Python 3.8+ 标准库）；复用 yotta-verify 内核（yotta_verify.py +
  verify_rules.py 规则表单源），不重复实现扫描逻辑，避免双实现漂移。
- 工具：① scan_skill（目录 / 包 → verdict + 发现）；② generate_badge（audited 徽章）；
  ③ gate_check（CI 闸门）；④ get_report（JSON / Markdown 报告）。
- 传输：stdio MCP（JSON-RPC 2.0，换行分隔），协议版本 2025-03-26。
- 边界：本地离线静态扫描；目录扫描完全离线；npm 包扫描仅下载公开包（不上传被测内容）；
  不执行被测代码；结论需人工确认。
- 形态：三个发布件（GitHub YottaMeta/yotta-verify-mcp + npm @yottameta/yotta-verify-mcp +
  ClawHub 元信 MCP）；MIT 开源发布。
- 测试：32 用例双版本（Python 3.8 / 3.13）全绿（含 stdio 端到端、恶意检测、错误入参）。
