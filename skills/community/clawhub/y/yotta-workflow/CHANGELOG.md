# Changelog

## v0.4.5 (2026-11-05)

- 发布包补 CHANGELOG；发布前测试接入。
- 发布门禁批次：发布工作流在 `npm publish` 前执行版本/发布面检查与 `npm test`；测试版本断言改为从 `package.json` 读取；补齐测试脚本。
- 打包与文档：发布包内容、CHANGELOG / README 与交付说明对齐；规则摘要与注册清单同步。

# 更新日志

## v0.4.4 (2026-11-01)

- 安装器 containment：目标根 / 嵌套链接 fail-closed；受管 Hub 链接解析真实目标；精简安装器同口径。

## v0.4.3 (2026-10-01)

- 安装器卫生批次：`bin/install.js` / `install.sh` 统一（未知参数报错 exit 2、`--help` / `--version`、残留清理白名单、嵌套载荷保留）；由模板单一真源渲染，接入漂移门禁。
- 自带安装器测试（`test/install.test.js`）更新为统一行为断言。

## v0.4.2 (2026-09-25)

维护性发布：README 安装命令锁定版本。

- README（中英）安装命令改为锁定版本写法（去掉 `@版本` 即跟随最新），配合元信对未锁定安装命令的提示。
- 安装器加固：拒绝对符号链接目标写入、不做整目录删除。

## v0.4.1 (2026-09-13)

**P0-4.4 元序 before_start / after_milestone 试点**：

- 新增 `skill-manifest.json`，声明 `before_start` / `read_state` 与 `after_milestone` / `write_state`。
- Codex 两个事件均为 `native-audit`：缺少状态文件证据或落盘失败时输出 `explicit-unverified` + 一次纠偏，不宣称动作前硬拦截。
- 元阁适配器回归验证 `file_path` 证据与里程碑纠偏结果。

## v0.4.0 (2026-09-10)

**路径模型澄清**：明确项目根目录、源码目录与工作区根目录的区别，采用“项目根目录 / `.workflow` / 源码目录”标准结构，避免把带 `.git` 的源码目录误当项目根目录。技能只规定标准形态；具体项目的源码布局由用户自行调整。

- 状态目录唯一位置明确为 `<项目根目录>\.workflow\`；项目根目录与源码目录可以重合，也可以嵌套。
- 定位收紧为两种证据：用户明确指定项目根目录，或向上找到已有 `.workflow`；两者都没有先问，不用 `.git`、`package.json`、`src`、`README`、cwd 或目录结构猜。已有 `.workflow` 永不自动迁移。
- 新增 `references/path-model.md`，补充单仓库、嵌套源码仓库、工作区多项目、从源码子目录开工四类走查。
- README 中英双版、FAQ、复杂场景走查、异常恢复手册同步统一术语。

## v0.3.0 (2026-09-08)

**评测驱动完善**：新增 FAQ、复杂场景走查与异常恢复手册；安装器错误处理与测试补齐。

- 新增 references/faq.md、walkthroughs.md、exception-playbook.md。
- 描述补齐边界：只记项目状态，不写 AI 人格、用户偏好、关系或跨项目通用知识。
- 安装器支持 --help、参数校验、统一退出码与人话错误提示。

## v0.2.6 (2026-08-29)

- 安装方式统一为四方式（对齐发布规范 §3.3.1）：方式一 `npx -y @yottameta/yotta-workflow --agent <name>` / `--dir <dir>`（推荐，走 npm 源）；方式二 `git clone https://github.com/YottaMeta/yotta-workflow.git`；方式三 GitHub Download ZIP；方式四 `bash install.sh --agent/--dir/--list`。移除 `npx skills` 与 `-g` 推荐；中英双 README 安装节同步。
- 版本对齐：package.json / SKILL.md / CHANGELOG / 引擎 VERSION / 测试断言 / README 锚点 = 0.2.6。
- 无功能变更（仅文档与版本同步）。

## v0.2.5 (2026-08-28)

中英双语文档：README.md（英文主文件，作为 GitHub / npm / ClawHub 主页） + 新增 README.zh-CN.md（中文全档）；安装方式统一为三方式（npx -g / --dir、install.sh、手动复制），移除 npx 固定 --agent codex（--agent 仅 install.sh 使用）；npm description 改英文；package.json files 加入 README.zh-CN.md。无功能变更。
