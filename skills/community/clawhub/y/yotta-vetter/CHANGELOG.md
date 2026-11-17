# Changelog

## v0.2.9 (2026-11-05)

- 修复 PRI-001 特殊权限位正则误报；刷新规则摘要；补授权与法律红线声明。
- 发布门禁批次：发布工作流在 `npm publish` 前执行版本/发布面检查与 `npm test`；测试版本断言改为从 `package.json` 读取；补齐测试脚本。
- 打包与文档：发布包内容、CHANGELOG / README 与交付说明对齐；规则摘要与注册清单同步。

# 更新日志

## v0.2.8 (2026-11-01)

- 安装器 containment：目标根 / 嵌套链接 fail-closed；受管 Hub 链接解析真实目标；精简安装器同口径。

## v0.2.7 (2026-10-01)

- 安装器卫生批次：`bin/install.js` / `install.sh` 统一（未知参数报错 exit 2、`--help` / `--version`、残留清理白名单、嵌套载荷保留）；由模板单一真源渲染，接入漂移门禁。

## v0.2.6 (2026-09-25)

安全修复：规则表豁免改为「路径 + 摘要绑定」。

- 背景：`collect_files()` 按文件名全局跳过 `audit_rules.py / vetter_rules.py / verify_rules.py / hardening_rules.py`——把恶意文件改成这些名字即可免扫（ClawHub T09 High）。
- 修复：豁免必须同时满足「相对路径为 `scripts/<规则表名>`（或扫描根就是 scripts 目录）」与「CRLF 归一化 SHA-256 命中已发布摘要表」；任一条不满足一律正常扫描（fail-closed）。
- 安装器加固：拒绝对符号链接目标写入、不做整目录删除。
- 回归：新增 4 项绑定用例，测试 16/16 通过。

## v0.2.5 (2026-09-19)

版本对齐维护：修复历史发布元数据与包内版本不一致；无功能变更。

## v0.2.3 (2026-08-30)

表述修正：统一对外表述。

## v0.2.2 (2026-08-30)

安全家族检测能力增强 + 措辞规范（与元信 / 元安 v0.2.2 对齐）：

- **报告升级（双视角）**：新增安全健康度评分（0-100） + 威胁捕获模型视图（8 检测点逐类 verdict） + 行为项（13 项），文本 / Markdown / JSON 三格式输出。
- **规则同步**：vetter_rules 同步元安权威源至 61 条（新增 路径穿越 / MCP 工具面命令执行 / MCP 工具面任意文件读写 检测器）。
- **措辞规范**：正文不再写版本号；统一对外表述（含代码注释与报告输出）。
- 测试：12 / 12 全绿（Python 3.8 / 3.13）。

## v0.1.5 (2026-08-29)

- 安装方式统一为四方式（对齐发布规范 §3.3.1）：方式一 `npx -y @yottameta/yotta-vetter --agent <name>` / `--dir <dir>`（推荐，走 npm 源）；方式二 `git clone https://github.com/YottaMeta/yotta-vetter.git`；方式三 GitHub Download ZIP；方式四 `bash install.sh --agent/--dir/--list`。移除 `npx skills` 与 `-g` 推荐；中英双 README 安装节同步。
- 版本对齐：package.json / SKILL.md / CHANGELOG / 引擎 VERSION / 测试断言 / README 锚点 = 0.1.5。
- 维护修复：签名数据文件跳过列表加入 hardening_rules.py。
- 无功能变更（仅文档与版本同步）。

## v0.1.4 (2026-08-29)

维护性修复（签名数据豁免）：

- 规则表豁免列表加入 `verify_rules.py`（yotta-verify 规则表）：元审检查 yotta-verify 时
  规则表自身字面量不再误报（keychain / id_rsa / DPAPI 等检测模式属签名数据）。

## v0.1.3 (2026-08-28)

中英双语 README 对齐 + 版本统一（英文门面 + 中文全档）：

- **README.md 改为英文**：作为 GitHub / npm / ClawHub 首页的英文门面（翻译 + 精简，覆盖定位 / 核心价值 / 四阶段协议 / 结论判定 / 使用示例 / 安装 / 升级卸载 / 常见问题 / 相关技能 / 边界 / 开发校验全流程）。
- **新增 README.zh-CN.md**：原中文完整主文档整体平移，顶部加语言切换链接。
- **移除 npx --agent codex 安装行**：README 安装方式一不再出现 `npx -y @yottameta/... --agent <name>`（固定智能体名，违反安装规范；npx 用 -g 或 --dir，--agent 仅 install.sh 用）。
- **版本统一 0.1.3**：此前 package.json=0.1.2、CHANGELOG 顶部=0.1.1、引擎 VERSION=0.1.0 不一致；本版统一为 0.1.3（package.json / SKILL frontmatter / 引擎 VERSION / CHANGELOG / 测试断言全对齐）。
- **package.json**：description 改英文；files 加 README.zh-CN.md。
- 边界（B 方案）：references / CHANGELOG / 测试注释不翻译；SKILL 触发描述保持中文。

## v0.1.1 (2026-08-26)

README 按标准补全：新增「这是什么 / 核心价值 / 核心优势 / 四阶段协议 / 结论判定 / 常见问题 / 相关技能 / 升级卸载」等章节，与 YottaMeta 技能矩阵 README 标准对齐；无功能变更。


## v0.1.0 (2026-08-26)

YottaMeta 自有实现首版（零依赖自研 + 中文教学）：

- check：四阶段初审（来源/代码/权限/风险）+ 危险模式规则扫描 + SKILL VETTING REPORT 报告。
- 危险模式规则与 yotta-security-audit（元安）共用（vetter_rules.py 为 audit_rules.py 的同步副本）。
- 联动元安（V3）：初审发现 high 及以上，输出深度扫描引导命令。
- source（V4）：GitHub 仓库来源半自动化检查（stars/更新时间/许可证），本地缓存，无网络自动降级。
- 输出：文本 / --json / --report report.md（SKILL VETTING REPORT 模板，含结论/决策记录/时间戳/审查者）。
- 零依赖（Python 3.8+ 标准库），Windows + Linux 通用，UTF-8 加固（GBK 控制台不崩）。
- exit code 语义与元安一致：0=干净/仅 low，1=medium，2=high，3=critical，4=错误。
- 版权：YottaMeta 纯自有 MIT + NOTICE 品牌声明。
