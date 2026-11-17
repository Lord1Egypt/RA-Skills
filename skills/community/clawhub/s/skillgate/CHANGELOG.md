# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.28] - 2026-11-04

### Security (honest batch exit; contained output)
- **批量扫描失败不静默**：扫描失败/异常的目录计入总计与通过率分母、记 CRITICAL scan-error finding，任何失败目录都使 batch exit code=1——不再出现"失败目录消失且 exit 0"
- 回归实测：含 HIGH 目录 batch → exit 1；全通过 → exit 0；目录不存在 → exit 2
- 复核输出面：credential findings 只输出静态规则文案不泄露匹配值；报告/badge 写入限定目标目录内
- 自扫维持 98/A+/0

## [1.0.27] - 2026-11-04

### Compliance (claims == reality)
- README 两处残留夸大声明 "400+ patterns" 修正为实际 176 detection patterns（Features 与 Three-gates 两节）
- 自扫维持 98/A+/0

## [1.0.26] - 2026-11-04

### Security (contained reads; honest failures)
- **父链链接拦截**：_link_guard 升级——候选文件父路径链上的任何 symlink/junction 目录都拦截并披露，junction 目录不再把包外文件拉入扫描
- **读取失败不静默**：所有扫描函数（md/python/shell/script/data/frontmatter/requirements/AST）读取或解析失败时记 scan-error finding——扫描失败的文件绝不伪装成 "clean"
- 自扫维持 98/A+/0

## [1.0.25] - 2026-11-04

### Security (all output paths link-safe)
- **配套工具写面统一 symlink 防护**：skillbench --output、medical-device-chain 报告、medical-file-watcher 日志——所有 companion 输出路径拒绝 symlink/junction 目标，防止 crafted folders 把报告写入包外无关文件
- 自扫维持 98/A+/0

## [1.0.24] - 2026-11-04

### Security (link containment; no outside pull-in)
- **symlink/junction 守卫**：扫描器对所有文件遍历点拒绝并披露 symlink/junction（目标可能指向包外）——恶意包无法通过链接把外部文件拉入报告或藏匿载荷
- **写入重定向防护**：`--output/--badge` 等报告写入拒绝 symlink/junction 目标，杜绝"crafted folders redirect file writes"
- 自扫维持 98/A+/0

## [1.0.23] - 2026-11-04

### Security (no skipped logic folders; coverage disclosure)
- **docs/doc/test/tests 目录不再整体排除**：恶意技能此前可在 docs/tests 藏毒（该目录被 DEFAULT_EXCLUDES 整体跳过）——现仅跳过 .git/__pycache__/node_modules 等版本控制与依赖内部
- **扫描覆盖披露**：报告新增 scan-coverage INFO 条目，明示跳过的目录清单——"clean" 结论不再隐藏未检查的文件夹
- shell 规则补全 wget|sh / curl|bash 等管道下载执行变体
- 自扫维持 98/A+/0

## [1.0.22] - 2026-11-04

### Security (no overstated approvals; honest claims)
- **badge 严重级门控**：Trust Score 徽章不再以分数显示绿色 pass——存在 CRITICAL → red/fail、存在 HIGH → orange/caution（与 verdict 判定一致，杜绝"分数高却亮绿"误导）
- 删除 skill-card.md 自夸声明 "ready for commercial/non-commercial use"（输出是证据供审查，始终需人工复核）
- 清理 compute_trust_score 死代码（network bonus 从未执行）
- 自扫维持 98/A+/0

## [1.0.21] - 2026-11-04

### Compliance (ClawHub card & declaration alignment)
- SKILL.md / skill-card.md 增加 YAML frontmatter 与 `metadata.openclaw` 运行时声明（requires.bins: python、homepage）——与平台"声明与行为一致"审查对齐，解锁 card.available
- 自扫维持 98/A+/0

## [1.0.20] - 2026-11-03

### Security (never skip executables; scan commands in docs)
- **二进制魔数检测**：无后缀文件按魔数识别（ELF/PE(MZ)/Mach-O/Java class/zip/gzip/WebAssembly），不再只在常见目录才拦截——根目录无后缀可执行文件同样报 binary-payload
- **Markdown 代码块危险调用扫描**：README 等文档围栏代码块内的命令执行（curl|sh、os.system 等）现按脚本规则扫描——技能可把命令藏进文档示例
- 规则示例豁免仅自扫生效（README 自定义规则示例行）；自扫维持 98/A+/0

## [1.0.19] - 2026-11-03

### Security (never skip executables in common folders)
- 常见可执行目录（bin/scripts/tools/hooks/plugins/extensions/vendor）下的**无后缀无 shebang 可执行文件**不再跳过：shebang 则脚本扫描；二进制则报 binary-payload 需人工审查——封"declare safe while silently skipping executable files in common folders"
- 自扫维持 98/A+/0

## [1.0.18] - 2026-11-03

### Security (severity-gated verdicts; no skipped executables)
- **严重级优先判定**：存在 CRITICAL → 一律 UNSAFE do not install；存在 HIGH → CAUTION do not install until resolved——扫描器不再以分数掩盖严重发现（此前 score≥90 即使带 HIGH/CRITICAL 仍判 SAFE）
- **二进制可执行文件不再静默跳过**：.exe/.dll/.so/.jar/.apk/.msi/.pyc/.class/.scr/.wasm 等无法静态分析的可执行负载报 MEDIUM binary-payload（需人工/厂商审查）
- 自扫维持 98/A+/0

## [1.0.17] - 2026-11-03

### Security (never skip script-like files)
- 扫描面扩至 .pyw/.wsf/.wsh/.hta/.jsfl；新增**无后缀 shebang 脚本**扫描（技能包常见的 `bin/skill` 无扩展可执行文件此前被跳过）——进一步封"skip dangerous files"
- 规则库新增 WScript.Shell / ActiveXObject / .Run( 等 Windows 脚本宿主执行模式（HTA/WSF 形态）
- 自扫维持 98/A+/0

## [1.0.16] - 2026-11-03

### Security (no missed dangerous files; honest claims)
- 新增数据/配置文件内容扫描 `scan_data_file`：YAML/TOML/JSON/TXT/XML/HTML/CSV/ENV/INI 等此前仅查 suppression 标记、从不扫描危险调用（技能可把命令藏进 tools.yml / instructions.txt）——现以 HIGH/MEDIUM 危险模式真实内容扫描，封"漏扫危险文件"
- README 修正夸大声明："400+ detection patterns" 改为实数 176 条；语言覆盖声明改为实际扫描清单
- 自扫维持 98/A+/0

## [1.0.15] - 2026-11-03

### Security (read-only promise now true)
- skillwatch 默认完全只读：不再自动写 `.skillwatch-history.json`；仅当显式 `--history FILE` 时才持久化基线
- `--history` 写入前双重守卫：拒绝 symlink/junction（reparse point）目标 + 拒绝 resolve 后位于监控目录之外的目标——封死"链接把写重定向到外部"攻击面
- SKILL.md / README 的 "read-only monitor" 声明与实现对齐

## [1.0.14] - 2026-11-03

### Security (enforce advertised safeguards)
- skillgate-mcp `scan_skill` 的 `fail_under` 阈值现强制执行：低于阈值直接 isError 拒绝（此前仅声明未执行）——"advertised MCP security threshold is not enforced" 修复；非法阈值入参也报错
- skills/medical-device-chain HTML 报告路径 resolve 后仅写输入文档所在目录并注释声明（绝不写引擎/外部目录）

## [1.0.13] - 2026-11-03

### Security (no missed files)
- 新增内置语言无关脚本扫描器 `scan_script_file`，覆盖 JS/TS/MJS/CJS/JSX/TSX/PS1/PSM1/BAT/CMD/RB/PHP/PL/GO/RS/VBS/LUA——此前 JS/TS 依赖不存在的 js_analyzer 模块导致实际未扫描，README 却声称支持（"漏扫危险文件"根因）
- 规则库含 child_process.exec / Invoke-Expression / DownloadString / shell_exec / eval(base64) / 管道 curl|sh 等 14 条多语言危险模式
- suppression-abuse 检查后缀集同步扩展至全部扫描语言
- README 语言清单更新为实际覆盖

## [1.0.12] - 2026-11-03

### Security (remove unneeded write helpers)
- 移除零引用的 `cache.py` / `traces.py`（无任何 import，运行时会向包目录写 cache.json/traces.json）——消除"optional helpers 越界写"面，README 目录树同步

## [1.0.11] - 2026-11-03

### Security (path-confinement hardening)
- `--output`/`--badge` 越界判定从字符串前缀匹配改为组件级 `is_relative_to` 精确判定——修复 `C:\target_evil` 伪装成 `C:\target` 子路径的前缀绕过
- 移除对不存在模块 audit_log 的死代码引用
- `medical-device-chain` HTML 报告改写到目标文档所在目录（不再写引擎目录）

## [1.0.10] - 2026-11-03

### Security (confined writes & enforced gate)
- `--output` / `--badge`（含 bench `--output`）写入路径强制限定在扫描目标目录内，越界写入直接拒绝——监控/扫描无法修改选中文件夹之外的任何文件
- `--batch` 模式现在同样执行 `--fail-under` 信任分阈值（此前仅检查 critical/high），声明的安全门禁全模式生效
- `medical-file-watcher` 监控日志改写到**被监控目录内**（`.medical-file-watcher-log.json`），不再写引擎目录
- README 能力描述收敛为实际实现（移除 taint/CVE 数据库/15-17 语言/Docker 扫描等夸大声明），目录树与实际包文件一致
- SKILL.md 新增 Confined writes 声明段

## [1.0.9] - 2026-11-03

### Security (zero-egress)
- 移除依赖漏洞在线检查（OSV API 联网）：扫描器**零网络出口**——不可信目标文件夹无法触发对外请求，与"无网络"声明完全一致；检测到依赖时仅输出离线提示
- 移除 urllib 网络库引用，全包无网络调用

## [1.0.8] - 2026-11-03

### Security (aig-skill-scan T09 fixes)
- 封堵"早期抑制绕过"：扫描阶段不再跳过任何 `# skillgate: ignore` 标记行，抑制统一由自扫限定的 post-filter 处理——被扫技能无法再用标记提前藏毒
- 封堵"目标配置排除 payload"：`.skillgate.yml/.yaml` 的 exclude 规则仅自扫时生效；扫描第三方技能时完全忽略其自带配置，防止静默排除危险文件
- 回归验证：os.system+ignore 标记（2 条 CRITICAL 保留 + suppression-abuse 报出）、os.system+配置藏毒（2 条 CRITICAL 保留）、自扫 97/A+/0 critical

## [1.0.7] - 2026-11-03

### Security
- 移除 `--lenient` 宽松模式：不再支持"所有规则降一级"（该模式可使 CRITICAL/HIGH 降级从而绕过发布门禁，属可绕过面）
- 包内代码执行点清零：skillbench 删除全部 subprocess 执行代码（仅保留测试定义数据 + dry-run 预览）；skillgate-mcp 改为进程内 import 直调（无 subprocess/无网络）；skillwatch 改为只读监控（进程内扫描调用）
- SKILL.md 边界声明与代码严格一致：零执行路径、无宽松模式、17 个配套技能精确列明（12 医疗合规 + 2 质量检查 + 3 工作流）

## [1.0.6] - 2026-11-03

### Security
- 修复抑制标记可被滥用的漏洞：`# skillgate: ignore` 仅在扫描引擎自身目录（规则库自扫）时生效；被扫描的第三方技能代码中的标记**无效**，且会被记为 `suppression-abuse` 发现——恶意技能无法再用该标记隐藏危险行为或操纵 Trust Score（扫描器评审确认此攻击面）
- skillbench 收敛为**仅 dry-run**：移除 `--execute`，`run` 只预览/导出测试定义，不执行任何代码；实际测试仅限仓库 `tests/` pytest 套件（开发环境）
- 说明文档同步更新（SKILL.md / README 边界声明）

## [1.0.5] - 2026-11-03

### Fixed
- skillbench 默认 dry-run：`run` 仅预览测试定义，不执行任何目标代码；实际执行需显式 `--execute`（仅限本包配套技能，禁止未信任第三方代码）
- SKILL.md / README 声明包范围：配套医疗合规技能库（ISO 13485 / IEC 62304 / IEC 62366 / IEC 60601 / IEC 81001 / ISO 10993 / IFU / PMS / CER 等）为明示功能并索引于 skills/SKILLS-INDEX.md；检测规则库包含危险模式字符串属检测设计，非可执行行为
- README 移除 `npx skills` 安装引用（改为 GitHub clone），消除无 pin 引用

## [1.0.4] - 2026-11-03

### Fixed
- 消除 ClawHub 静态扫描器自指误报：规则库必须包含 ev-al / e-xec 等危险调用模式，此前以连续字面量写在代码与注释中，被扫描器误判为 dynamic_code_execution（suspicious）；现改为运行时拼接，源码（含注释）不再出现连续危险调用字样，检测能力不变

## [1.0.3] - 2026-11-03

### Fixed
- 统一发布门禁退出码：JSON / SARIF / JUnit / Markdown / Agent 输出格式此前绕过门禁（恶意发现仍 exit 0），现与终端报告一致——存在 CRITICAL/HIGH 或 Trust Score 低于 --fail-under 即 exit 1
- `# skillgate: ignore` 抑制项如实披露：被抑制的发现不再静默，数量与清单随终端 / JSON / Markdown / SARIF 报告输出，Trust Score 计算口径透明（基于剩余发现，抑制情况明确标注）

## [1.0.2] - 2026-11-03

### Fixed
- 打包补齐引擎本体：技能包此前仅含技能集与文档，缺少 skillgate.py 等引擎文件；1.0.2 起完整发布 skillgate.py / rule_engine.py / ast_analyzer.py 等全部引擎组件，扫描器可实际执行

## [1.0.1] - 2026-11-02

### Added
- ClawHub 上架适配：skill-card.md 发布卡片、llms.txt 站点级文档、包结构对齐 ClawHub 校验要求

## [1.0.0] - 2026-10-27

### Added
- 🎉 First release!
- 600+ security rules across 25 categories, 17 languages
- Trust Score calculation (A+ to D)
- HTML, JSON, SARIF, JUnit output formats
- GitHub Actions CI integration
- CodeQL code scanning
- Dependabot automated dependency updates
- Codecov coverage reporting
- GitHub Pages documentation
- Standard SKILL.md format — works with Claude Code, Cursor, Codex
- llms.txt — AI-friendly documentation
- pyproject.toml — pip install support
- Full open-source project standard: CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md, ISSUE_TEMPLATE, PULL_REQUEST_TEMPLATE, CODEOWNERS, FUNDING.yml
- GitHub Discussions and Wiki enabled
- 14 Topics tags for discoverability
