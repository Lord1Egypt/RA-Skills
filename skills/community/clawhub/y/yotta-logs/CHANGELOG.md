# Changelog

## v0.3.5 (2026-11-05)

- 质量门禁与打包文档修正；发布前测试接入。
- 发布门禁批次：发布工作流在 `npm publish` 前执行版本/发布面检查与 `npm test`；测试版本断言改为从 `package.json` 读取；补齐测试脚本。
- 打包与文档：发布包内容、CHANGELOG / README 与交付说明对齐；规则摘要与注册清单同步。

## v0.3.4 (2026-11-01)

- 安装器 containment：目标根 / 嵌套链接 fail-closed；受管 Hub 链接解析真实目标；精简安装器同口径。

## v0.3.3 (2026-10-01)

- 安装器卫生批次：`bin/install.js` / `install.sh` 统一（未知参数报错 exit 2、`--help` / `--version`、残留清理白名单、嵌套载荷保留）；由模板单一真源渲染，接入漂移门禁。
- 自带安装器测试（`test/install.test.js`）更新为统一行为断言。

## v0.3.2 (2026-09-25)

安全修复：URL 内嵌凭据脱敏覆盖所有协议 + 查询串凭据。

- 背景：默认脱敏只处理 `http(s)://user:pass@`，`postgres://user:secret@…` 这类连接串与 `?token=…` 查询串会原样保留（ClawHub T09 Medium）。
- 修复：用户信息脱敏扩展到任意 `scheme://user:pass@`；新增查询串凭据遮蔽（`token / api_key / access_token / password / secret / sig` 等参数值替换为 `***`），非凭据参数保持不变。
- 安装器加固 + README 安装命令补锁定版本写法。
- 回归：新增 3 项脱敏用例，测试 146/146 通过。

- 修复本机专属路径硬编码：移除本机自定义数据目录候选；opencode 只认 `XDG_DATA_HOME` / `OPENCODE_DATA` / 官方默认路径，Codex notes 只认 `$CODEX_HOME/memories` 或 `~/.codex/memories`。
- 配置路径改为平台无关：`$YOTTA_LOGS_CONFIG` > Windows `%APPDATA%` > Unix `$XDG_CONFIG_HOME` / `~/.config`。
- 新增便携覆盖回归：`YOTTA_MEMORY_HOME`、`CODEX_HOME`、`YOTTA_LOGS_CONFIG`；并加本机自定义目录反向断言。

## v0.3.1 (2026-09-13)

## v0.3.0 (2026-09-08)

**评测驱动完善**：新增 FAQ，安装器错误处理与测试补齐。

- 新增 references/faq.md，覆盖格式、范围、脱敏、只读边界与安装排障。
- 安装器支持 --help、参数校验、统一退出码与人话错误提示。

# 更新日志

## v0.2.2 (2026-08-29)

- 安装方式统一为四方式（对齐发布规范 §3.3.1）：方式一 `npx -y @yottameta/yotta-logs --agent <name>` / `--dir <dir>`（推荐，走 npm 源）；方式二 `git clone https://github.com/YottaMeta/yotta-logs.git`；方式三 GitHub Download ZIP；方式四 `bash install.sh --agent/--dir/--list`。移除 `npx skills` 与 `-g` 推荐；中英双 README 安装节同步。
- 版本对齐：package.json / SKILL.md / CHANGELOG / 引擎 VERSION / 测试断言 / README 锚点 = 0.2.2。
- 无功能变更（仅文档与版本同步）。

## v0.2.1 (2026-08-27)

文档中英双版：

- **README.md 改为英文**：作为 GitHub / npm / ClawHub 首页的英文门面（翻译 + 精简，覆盖定位 / 核心价值 / 命令 / 快速使用 / 安装 / 使用示例 / 开发校验全流程）。
- **新增 README.zh-CN.md**：原中文完整主文档整体平移，继续服务中文用户，顶部加语言切换链接。
- **package.json**：description 改英文；files 加 README.zh-CN.md；版本 0.2.0 → 0.2.1。
- 版本四处对齐：package.json / SKILL frontmatter / 引擎 VERSION / 文档。
- 边界（B 方案）：references / CHANGELOG / 测试注释不翻译；SKILL 触发描述保持中文。

## v0.2.0 (2026-08-27)

多格式通用化：不再只认 JSONL，按「格式族 × 字段别名归一 + 配置兜底」适配一切格式：

- **五大格式族 reader**：JSONL（支持嵌套子目录与 Codex rollout payload 形态）/ 单文件 JSON（数组、dict-of-lists）/ SQLite（opencode schema 实测 + 通用列映射兜底，只读 mode=ro）/ Markdown（YAML frontmatter 结构化记忆 + 自由笔记）/ 二进制（只降级读标题不崩）。
- **统一 Record 模型**：{source, format, kind, session, time, role, text, path, meta}；字段别名归一（time / role / text / session / title），秒 / 毫秒自动推断，JSON 字符串解包。
- **discover 全源登记**：locate 遍历所有 reader 的 discover()，登记 Codex / Claude Code / Clawdbot / opencode（XDG_DATA_HOME / OPENCODE_DATA / 默认路径）/ VS Code·Cursor state.vscdb / Continue / yotta-memory（memory_home 配置）/ Codex 笔记 / Aider / Windsurf 等已知根。
- **配置兜底**：~/.config/yotta-logs/config.json（$YOTTA_LOGS_CONFIG 覆盖），sources[] 自定义源（table / col_time / col_role / col_text / col_session / col_title），引擎零改动接入怪格式。
- **过滤与默认范围**：新增 --source / --kind / --format；默认检索范围 = 会话源 + 结构化记忆源开，自由笔记 / 二进制日志关（可显式开）。
- 测试：139 项全绿（75 项 v0.1.0 回归 + 64 项 v0.2.0 通用化用例）；py_compile / validate-skill / 元安 / 元审全过。
- 文档：新增 references/agent-formats.md 普查登记表；format.md / cli.md / security.md / SKILL.md / README.md 同步；版本 0.1.0→0.2.0 四件对齐（package.json / SKILL frontmatter / 引擎 VERSION / 文档）。

## v0.1.0 (2026-08-27)

YottaMeta 自有实现首版（历史会话日志检索方向参考开源社区 session-logs 类技能思路，已完全重写）：

- 元史（yotta-logs）—— 零依赖跨智能体会话日志检索引擎（Python 3.8+ 标准库）。
- 能力：locate / scan / search / session / stats / tools / version；关键词 / 正则 / 日期 / 会话 ID / 别名 / 角色过滤；默认脱敏（--no-redact 关闭）；--json 结构化输出；只读安全；容错 JSONL 解析（含 sessions.json 索引别名）。
- 测试：scripts/test_yotta_logs.py 75 项全绿。
- 版权：YottaMeta 纯自有 MIT + NOTICE 品牌声明。
