# Changelog

## v1.4.4 (2026-11-05)

- 发布包补 CHANGELOG；发布前测试接入。
- 发布门禁批次：发布工作流在 `npm publish` 前执行版本/发布面检查与 `npm test`；测试版本断言改为从 `package.json` 读取；补齐测试脚本。
- 打包与文档：发布包内容、CHANGELOG / README 与交付说明对齐；规则摘要与注册清单同步。

## v1.4.3 (2026-11-01)

- 安装器 containment：目标根 / 嵌套链接 fail-closed；受管 Hub 链接解析真实目标；精简安装器同口径。

## v1.4.2 (2026-10-01)

- 安装器卫生批次：`bin/install.js` / `install.sh` 统一（未知参数报错 exit 2、`--help` / `--version`、残留清理白名单、嵌套载荷保留）；由模板单一真源渲染，接入漂移门禁。
- 自带安装器测试（`test/install.test.js`）更新为统一行为断言。

## v1.4.1 (2026-09-25)

口径修正：明确本规则不覆盖用户指令（ClawHub T01）。

- 背景：核心原则块里的 `[ROLE]` 优先级声明被判为「持续指令覆盖用户意图」。
- 修复：`priority` 改为 `preference`（限定在用户给定目标与项目规则之内），并新增 `[LIMITS]`：质量自检清单不覆盖用户明确指令与项目规则、不扩权、不代替测试与人工复核，用户说「免规则 / 直接做」立即让位。
- 安装器加固：拒绝对符号链接目标写入、不做整目录删除。

**评测驱动完善**：新增 FAQ 与复杂场景走查，补齐轻量 / 完整自检判定，安装器错误处理与测试补齐。

- 新增 references/faq.md 与 references/walkthroughs.md。
- 描述补齐边界：质量纪律规则，不执行代码，不替代测试或人工复核。
- 安装器支持 --help、参数校验、统一退出码与人话错误提示。

# 更新日志

## v1.4.0 (2026-09-08)

## v1.3.4 (2026-08-29)

- 安装方式统一为四方式（对齐发布规范 §3.3.1）：方式一 `npx -y @yottameta/yotta-anti-shallow --agent <name>` / `--dir <dir>`（推荐，走 npm 源）；方式二 `git clone https://github.com/YottaMeta/yotta-anti-shallow.git`；方式三 GitHub Download ZIP；方式四 `bash install.sh --agent/--dir/--list`。移除 `npx skills` 与 `-g` 推荐；中英双 README 安装节同步。
- 版本对齐：package.json / SKILL.md / CHANGELOG / 引擎 VERSION / 测试断言 / README 锚点 = 1.3.4。
- 无功能变更（仅文档与版本同步）。

## v1.3.3 (2026-08-28)

中英双语文档：README.md（英文主文件，作为 GitHub / npm / ClawHub 主页）+ 新增 README.zh-CN.md（中文全档）；安装方式统一为三方式（npx -g / --dir、install.sh、手动复制），移除 npx 固定 --agent codex；npm description 改英文；package.json files 加入 README.zh-CN.md；SKILL.md 移除内嵌「版本历史」表（统一用独立 CHANGELOG.md）。无功能变更。
