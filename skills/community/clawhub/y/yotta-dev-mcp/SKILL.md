---
name: yotta-dev-mcp
slug: yotta-dev-mcp
version: 0.2.8
displayName: 元开·确定性开发工具
summary: 元开（yotta-dev-mcp）—— 本地、确定性的开发工具 MCP：18 个工具覆盖代码库地图、架构契约与系统模型、架构评审、变更影响锥、验证账本与反证自测、可选适配器、代码评审、密钥 / 依赖扫描、发布前守门、白名单检查、技能脚手架与 workflow 状态；默认离线、默认只读、带证据锚点。
description: '元开（yotta-dev-mcp）—— 一个 stdio MCP server 提供 18 个确定性开发工具：repo_map（代码库地图）、system_model（系统模型与 .yotta/architecture.json 契约分层）、architecture_review（契约评审）、impact_analysis（变更影响锥）、verify_change（L0-L5 验证账本）、self_test（完整性检查与 seeded defect / mutation 反证）、run_adapter（显式运行 import-linter / dependency-cruiser / Repomix）、find_code（符号定位）、compress_output（长输出压缩）、review_code / review_diff（规则化评审）、scan_secrets（密钥脱敏扫描）、scan_dependencies（依赖与 typosquat 启发式）、check_publish_readiness（发布前守门）、run_checks（白名单检查，默认关闭执行）、scaffold_skill（技能脚手架，默认 dry-run）、workflow_state（.workflow 状态读取与安全追加）。Python 3.8+ 标准库、默认离线、默认只读、输出带文件行号与规则证据；缺工具或配置一律 UNKNOWN，不自动安装、不联网。'
tags: [MCP, 开发能力, 代码库地图, 架构评审, 影响分析, 验证账本, 代码评审, 密钥扫描, 依赖检查, 发布检查, developer tools, code review, repo map]
category: dev-programming
license: MIT
homepage: https://github.com/YottaMeta/yotta-dev-mcp
---
# 元开（yotta-dev-mcp）

元开（YuanKai）把一组本地、确定性的开发工具做成一个 stdio MCP server。任何支持 MCP 的客户端接上后，
都能在真实开发任务里调用这些工具；输出带文件、行号、规则和证据，便于直接进入修复清单。

## 何时使用

- 接手陌生项目：先 `repo_map` 看模块、依赖和入口，再 `find_code` 定位。
- 架构与影响分析：先写 `.yotta/architecture.json`，再用 `system_model` 拿分层、依赖、测试映射与 `UNKNOWN` 清单。
- 契约评审：用 `architecture_review` 查依赖规则、边界可见性与数据归属，每条给证据与严重级。
- 改动前评估：用 `impact_analysis` 从改动文件 / diff / 目标符号走出影响锥、映射测试与回滚探针。
- 改动后验证：用 `verify_change` 跑 L0 / L1 默认检查，按需结合 `.yotta/verification.json` 与 `allow_execute=true` 执行 L2-L4 白名单检查，产出可复算账本。
- 自身完整性：用 `self_test` 检查文件、版本、工具契约、写闸门与 seeded defect / mutation 反证。
- 可选增强：用 `run_adapter` 先 `action=list` 探测 import-linter / dependency-cruiser / Repomix，再按需 `action=run` + `allow_execute=true`；缺工具或配置返回 UNKNOWN，不自动安装、不自动下载。
- 评审改动：`review_diff` 只看新增行；`review_code` 对文件或仓库做规则检查。
- 长日志 / 长命令输出：`compress_output` 保错误、错误栈和首尾上下文。
- 本机排查：`mcp_doctor` 只读发现多宿主 / 多根 MCP 配置（JSON / JSONC / TOML 子集）与技能目录覆盖，返回 coverage；只列 server 名，不含 command / env。

## MCP 接入

启动命令：

```bash
npx -y @yottameta/yotta-dev-mcp@0.2.8
```

`npx -y` 是 npx 的自动安装开关，不是安装器的 `--yes`；`-g/--global` 不再强制 `--yes`。

或直接用本地脚本：

```bash
python scripts/yotta_dev_mcp.py
```

工具分组（`--tools`，与元忆同口径）：

```bash
python scripts/yotta_dev_mcp.py --tools core   # 5 工具：repo_map / find_code / review_code / review_diff / verify_change
python scripts/yotta_dev_mcp.py --tools full   # 18 工具（默认）
```

`core` 给「需要把工具表常驻在上下文里」的宿主用：schema 体积约为 `full` 的 29%
（5 工具 3,883 字符 vs 18 工具 13,230 字符，紧凑 JSON 口径），适合默认启用；
`full` 暴露全部工具，适合按需调用、不常驻的场景。`core` 模式下调用 full 专属工具会返回
明确提示（提示用 `--tools full` 重启）。

运行期自检：先看客户端 `tools/list` 实际返回。只有 5 个工具即 core 档；需要
`system_model` / `architecture_review` 等 full 专属工具时，用 `--tools full` 重启。
服务端不会在 `tools/list` 之外补发隐藏工具，legacy `initialize` 与 modern
`server/discover` 都会在 instructions 中报告当前档位。

自动接入说明：AI 首次协助配置时，必须先展示目标配置文件、完整配置片段和影响，
并获得用户明确同意后再写入 `mcpServers`。用户拒绝时不要写文件，直接提供上面的启动命令
让用户手动接入。

## 工具

| 工具 | 用途 | 写入 |
|---|---|---|
| `repo_map` | 模块、导入、入口点地图；支持 `from . import X` / 别名 / 包，忽略临时与探针目录 | 否 |
| `system_model` | 系统模型：模块、依赖、入口、测试映射、配置与数据归属；附带契约分层，输出 PASS / FAIL / UNKNOWN | 否 |
| `architecture_review` | 按契约评审依赖规则、边界可见性与数据归属；critical / high 判 FAIL，medium / low 只告警 | 否 |
| `impact_analysis` | 变更影响锥：直接消费者、受影响层 / 边界 / 存储 / 不变量、映射测试、风险分级与回滚探针 | 否 |
| `verify_change` | L0-L5 验证阶梯与证据账本：L0 / L1 默认，L2-L4 需策略声明 + 显式执行，L5 始终留在未验证项 | 仅显式 allow_execute 的 L2-L4 |
| `self_test` | source 档：文件 / 版本 / 工具契约 / 写闸门 / 反证；installed 档：文件 / 版本 / 反证（3 项） | 仅显式 allow_execute 的测试子集 |
| `run_adapter` | 探测或显式运行 import-linter / dependency-cruiser / Repomix；固定 argv、项目内 cwd、有界输出与哈希 | 仅 action=run + 显式 allow_execute |
| `find_code` | 符号 / 文本定位，结果有上限 | 否 |
| `compress_output` | 保留错误与首尾的长输出压缩 | 否 |
| `review_code` | 规则化代码评审，带行号与建议；忽略 `.workflow` / `scratch` / `_probe` 等临时目录 | 否 |
| `review_diff` | 只评审 diff 的新增行；`base` 先解析为 commit SHA，拒绝选项注入 | 否 |
| `mcp_doctor` | 技能版本与多宿主 / 多根 MCP 配置（JSON / JSONC / TOML 子集）体检；返回 coverage，只列 server 名，不含 command / env | 否 |
| `scan_secrets` | 密钥 / 凭据 / 高熵令牌扫描（强制脱敏；路径 / 哈希 / 文件名噪声过滤） | 否 |
| `scan_dependencies` | 依赖清单、lockfile、来源与 typosquat 启发式检查 | 否 |
| `check_publish_readiness` | 版本四件、发布文件、仓库与 publishConfig 检查 | 否 |
| `run_checks` | 白名单测试 / lint / compile 并返回结构化摘要 | 仅显式 allow_execute |
| `scaffold_skill` | 生成最小技能脚手架，默认 dry-run | 仅显式 apply |
| `workflow_state` | 读取 `.workflow`，可选显式追加日志；写入拒绝链接路径并使用原子替换 | 仅显式 apply |

详细契约见 `references/tools.md`；架构契约、评审语义与影响锥字段见 `references/architecture-contract.md`。

## 边界

- 会执行项目代码的工具默认关闭：`run_checks`、`verify_change` 的 L2-L4 策略检查、`self_test` 的测试子集都必须显式 `allow_execute=true`，且只运行白名单检查或已声明的策略检查。
- 外部适配器只在用户已安装时接入：`run_adapter` 不安装、不下载、不访问远端、不接收任意命令参数；工具缺失或配置缺失一律返回 `UNKNOWN` 并给出 next_step。
- `scaffold_skill` / `workflow_state` 默认只预览，显式 `apply=true` 才写入；脚手架拒绝覆盖已有非空目录，状态写入使用原子替换并为被覆盖文件保留 `.bak`。
- `workflow_state` 写入会拒绝目标或祖先路径中的 symlink / junction 等链接重定向；
  临时文件使用随机独占名，避免可预测 `.tmp` / `.bak` 路径被预置链接利用。
- `review_code` / `review_diff` 支持 `.review-allowlist.json`（或 `.yotta/review-allowlist.json`）精确豁免（path + rule + line + reason，无通配符）；非法配置 fail-closed，不抑制 findings。
- `review_diff` 的 `base` 必须是可解析 Git revision；以 `-` 开头、含空白或无法解析的值会被拒绝，
  防止 `--output=` 等选项注入。
- 不联网，不查询包是否存在于公共仓库。
- 不读取或修改 YottaCode 仓库。
- 结论是确定性静态判断，不替代人工评审与最终决策。

## 当前版本

- v0.2.8（2026-11-05）：质量门禁批次——发布前测试接入；测试子进程统一 UTF-8；自扫测试样本去字面量；版本五件对齐。
- v0.2.7（2026-10-31）：BOM 契约修复——`.yotta/architecture.json`、`.yotta/verification.json`、changed `.py` / `.json`、adapter 配置、custom host registry 与 `--diff-file` 的结构化读取统一 `utf-8-sig`；修正 BOM 契约假绿用例，新增 BOM 矩阵、静态编码门禁与 RED→GREEN 证据；测试规范见 `docs/元开-测试规范-2026-10-31.md`。
- v0.2.5（2026-10-31）：安全热修——`review_diff` 的 `base` 先解析为 commit SHA，拒绝 Git 选项注入；`workflow_state` 改为随机独占临时文件 + 原子替换，备份同样原子化，并拒绝 symlink / junction 等链接路径；新增 option injection、temp / backup / hardlink / junction 回归。
- v0.2.4（2026-10-31）：外部缺陷报告修复——`architecture_review` 修 BOM 假 PASS 与零证据 PASS；legacy `initialize` 报告当前工具档位；`review_code` / `review_diff` 修 `.exec(` 与字符串内待办标记误报并新增精确 allowlist；补齐临时 / 备份目录忽略；`scan_secrets` 补弱口令并去重；`find_code` 支持 `def ` 前缀；`self_test` 增加当前版本正文检查。
- v0.2.3（2026-10-01）：安装器卫生批次——`bin/install.js` / `install.sh` 统一，未知参数 exit 2、`--help` / `--version`、残留清理白名单与嵌套载荷保留。
- v0.2.2（2026-09-26）：新增 `--tools core|full` 工具分组；core 5 工具 / full 18 工具，core 拒绝 full 专属工具。
- v0.2.1（2026-09-25）：缺陷修复批次——`mcp_doctor` 改为多宿主 / 多根 / JSON+JSONC+TOML 子集发现并返回 coverage；`self_test(mode="installed")` 按精简分发副本 / npm / plugin / r0 形态判断 banner；`repo_map` 修复 `from . import X` 解析；`scan_secrets` 过滤路径 / 哈希 / 文件名噪声；`review_code` / `repo_map` 忽略 `.workflow` / `scratch` / `_probe` 等临时目录。
- v0.2.0（2026-09-25）：新增 `system_model`、`architecture_review`、`impact_analysis`、`verify_change`、`self_test`、`run_adapter`，以及 `.yotta/architecture.json` 与可选 `.yotta/verification.json` 契约（版本 1）；工具总数 18，原 12 个工具行为不变。
- v0.1.1：品牌显示名统一为「元开」；功能与 12 个工具不变。
