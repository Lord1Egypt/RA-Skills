# Changelog

## v0.3.6 (2026-11-05)

- 修复 PRI-001 特殊权限位正则误报；刷新家族规则表摘要；发布门禁补 license 与摘要检查。
- 发布门禁批次：发布工作流在 `npm publish` 前执行版本/发布面检查与 `npm test`；测试版本断言改为从 `package.json` 读取；补齐测试脚本。
- 打包与文档：发布包内容、CHANGELOG / README 与交付说明对齐；规则摘要与注册清单同步。

# 更新日志

## v0.3.5 (2026-11-01)

- 安装器 containment：目标根 / 嵌套链接 fail-closed；受管 Hub 链接解析真实目标；精简安装器同口径。

## v0.3.4 (2026-10-01)

- 安装器卫生批次：`bin/install.js` / `install.sh` 统一（未知参数报错 exit 2、`--help` / `--version`、残留清理白名单、嵌套载荷保留）；由模板单一真源渲染，接入漂移门禁。
- 安装器版本改读 `package.json`（去掉硬编码 VERSION）。

## v0.3.3 (2026-09-25)

安全修复：不可静态分析的可执行载荷 fail-closed + tarball 解包上限（重新发布到 ClawHub，带回 v0.3.2 的豁免收紧）。

- 背景：v0.3.2 的「规则表豁免改为路径 + 摘要绑定」没能进入 ClawHub 公开版本体系（公开版本历史停在 0.3.1），本次以 0.3.3 重走发布链。
- 新增 `STR-009`：包内含无法静态分析的可执行 / 二进制文件（`.exe` `.dll` `.so` `.jar` 等扩展名，或 ELF / MZ / Mach-O 魔数）时按 medium 报出并让结论至少为「需复核」，不再静默跳过。
- tarball 解包加三道上限：成员数 2000 / 单成员 50 MB / 解包总量 200 MB，超限直接拒绝。
- 安装器加固（符号链接目标拒绝、不做整目录删除）；README 安装命令补锁定版本写法。
- 回归：新增 5 项用例，测试 81 项全绿。

## v0.3.2 (2026-09-19)

安全修复：签名数据豁免与检测器降级改为「路径 + 内容摘要」双绑定。

- 背景（平台扫描发现）：旧实现按**文件名**全局跳过 `verify_rules.py` / `audit_rules.py` /
  `vetter_rules.py` / `hardening_rules.py`，且 `is_detector_skill()` 仅凭「目录里出现同名文件」
  判定检测型技能。两点都可被伪造：把恶意文件命名成规则表即可逃避扫描；放一个同名标记文件即可把
  整包文档命中降级为 info。
- 修复：
  - 规则表豁免必须同时满足 ① 相对路径恰为 `scripts/<规则表名>.py`；② 文件 SHA-256（CRLF 归一化）
    命中「已发布规则表摘要表」；任一条不满足 → 正常扫描（fail-closed）。
  - `is_detector_skill()` 改由上述摘要绑定判定，标记文件不再触发文档降级。
  - `test_*.py` 跳过只对「持有已发布签名数据」的自家包生效；非自家包的同名文件照常扫描
    （发布包已用 `!scripts/test_*.py` 排除测试文件，发布物不受影响）。
- 维护约定：任一家族规则表（四张表中任意一张）改动后，必须同步刷新 `SIGNATURE_DATA_DIGESTS`；
  根仓库 `tools/check_rule_digests.py` 提供一致性校验（漏更新会在自扫时明显报错，不会静默放行）。
- 纳入元盾规则表：`guardian_rules.py` 同样按「路径 + 摘要」绑定加入签名数据集合——元盾是检测型
  技能，其文档中对危险命令的描述属固有属性，本版本起按检测技能文档降级处理（此前会误报
  PIJ-020 / NET-008，导致其发布副本自扫为 INSTALL WITH CAUTION）。
- 测试维护：`test_yottamemory_clean` 的过时断言（按 v0.8.5 期望 SAFE）校正为家族技能门禁口径
  （无 critical / high），并注明 loopback `fetch` 命中 NET-007 为已知可读性提示。
- 验证：`scripts/test_yotta_verify.py` 79/79；家族 26 技能源码自扫对比仅 2 项变化
  （元察 / 元析各 +2 medium，均位于发布包已排除的 `scripts/test_*.py`）。

## v0.3.1 (2026-09-14)

**STR-004 误报修复**：

- npm tarball 与解压后的 `package/` 根目录不再用临时目录名或压缩包文件名做 STR-004 比对；改为从根 `package.json` 的 `name` 推导期望 slug。
- 真实安装目录名不一致、`package.json` 名称与 frontmatter name 不一致时仍保留 STR-004 medium。
- 检测型技能的文档降级不再吞掉 `Structure` 类发现，真实错目录名仍保留 STR-004 medium。
- 新增回归：`package/` 目录、npm tarball、真实错目录名、错 package name。
- 安全加固：tarball 解压拒绝符号链接、硬链接、设备与 FIFO 成员，Python 3.12+ 叠加官方 `data` 过滤器；新增两组链接成员回归。

## v0.3.0 (2026-09-13)

**P0-4.1 元信 before_install 试点**：

- 新增 `skill-manifest.json`，声明 `before_install` / `scan_skill` / `on_fail: block` / `fallback: wrapper`。
- 发布工作流 `.github/workflows/publish.yml` 纳入版本库，标签推送可触发 GitHub Actions。
- 元阁安装管线通过统一 hook 适配器评估 `before_install`，扫描不通过时阻断落位并保留旧版本。
- 适配器证据写入 `~/.yottaskills/hook-log.jsonl`，安装证据仍写 `install-log.jsonl`。
- 发布件包含 `skill-manifest.json`，供元阁安装器读取。

## v0.2.2 (2026-08-30)

- 措辞规范：正文不再写版本号；统一对外表述。


## v0.2.0 (2026-08-30)

安全家族检测能力增强（8 检测点威胁捕获模型 + 13 行为项）：

- **威胁捕获模型**：官方 8 检测点 taxonomy（供应链风险 / 命令执行风险 / 网络请求与数据外传 /
  文件操作与敏感路径访问 / Prompt 注入风险 / 远程脚本下载执行 / 可疑编码·混淆 / 其他安全风险）。
- **L3 MCP 工具面引擎（新增）**：识别 MCP server 工具集，追踪「工具参数 → 危险 sink」
  （spawnSync/execSync/任意文件读写），恶意 MCP 判 DO NOT INSTALL
  （修复差距实证：此前只报 info 权限汇总不判级）。
- **L2 数据流引擎（新增）**：argv 注入面 → 子进程 sink 无防护判 medium。
- **L1 判级修正**：新增 PathTraversal（路径穿越）/ MCPCommandExec（MCP 命令执行）/
  MCPFileAccess（MCP 任意文件读写）检测器（audit_rules 权威源，规则 54 → 61）。
- **报告升级双视角综合报告**：安全健康度评分（0-100）+ 威胁捕获模型视图（8 类逐类 verdict）+
  行为项（13 项）+ 逐文件 verdict + 修复建议指南 + 内容 hash（text / JSON / Markdown）。
- **自扫与正例保障**：元信自扫 SAFE；yotta-memory v0.8.5（修复后）正例 SAFE；
  恶意 MCP 样例 DO NOT INSTALL；测试文件（构造样例）扫描跳过、发布包排除测试。
- **测试**：67 / 67 全绿（Python 3.8 / 3.13）。

## v0.1.1 (2026-08-29)

维护性修复：

- 签名数据豁免：SIGNATURE_DATA_FILES 增加 hardening_rules.py（元安规则表），扫描元安
  （yotta-agent-hardening）仓库时不再把规则签名表误报为被测代码；与元安 S4 发布后家族
  规则表结构对齐（2026-08-29 升版）。

## v0.1.0 (2026-08-29)

初始发布：

- 定位：元信 —— 装前安全扫描器 + audited 徽章（信任层，市场主线 M1「已验证安全」）。
- 引擎：零依赖（Python 3.8+ 标准库）装前安全扫描 CLI，四块检测：
  ① Prompt Injection 8 类 28 条规则（指令覆盖 / 角色伪造 / 编码指令 / 数据外传 / 分隔符逃逸 /
     工具自执行 / 隐藏意图 / 凭据采集）+ base64 编码指令启发式；
  ② 危险模式 54 条规则（与元安 audit_rules 同步副本：下载即执行 / 混淆 / 持久化 / 外传 /
     凭据窃取 / 网络调用 / 权限提升 / 社会工程）；
  ③ SKILL.md 完整性（frontmatter 必需字段 / name 一致 / 围栏平衡 / 占位符）；
  ④ 权限需求分析（网络 / 命令 / 写入 / 敏感读取，info 级提示）。
- verdict：SAFE TO INSTALL / REVIEW REQUIRED / INSTALL WITH CAUTION / DO NOT INSTALL；
  exit code 与元安 / 元审一致（0 / 1 / 2 / 3 / 4）。
- badge：audited 徽章（本地 SVG + shields.io URL），内容 = verdict + validate-skill +
  元安 / 元审 verdict + 版本 + 引擎测试数。
- report：SKILL VERIFY REPORT（Markdown / JSON）。
- gate：CI 装前闸门（--max-severity，默认 medium，超出即失败）。
- 核心功能全开放。
- 测试：52 用例全绿（含自扫 dogfooding 无中高危）。
- 文档：SKILL.md + README 中英双版 + references（注入模式 / 报告模板 / 徽章说明）。
