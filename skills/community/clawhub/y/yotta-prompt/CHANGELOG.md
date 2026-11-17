# Changelog

## v0.2.6 (2026-11-05)

- 质量门禁与打包文档修正；发布前测试接入。
- 发布门禁批次：发布工作流在 `npm publish` 前执行版本/发布面检查与 `npm test`；测试版本断言改为从 `package.json` 读取；补齐测试脚本。
- 打包与文档：发布包内容、CHANGELOG / README 与交付说明对齐；规则摘要与注册清单同步。

## v0.2.5 (2026-11-01)

- 安装器 containment：目标根 / 嵌套链接 fail-closed；受管 Hub 链接解析真实目标；精简安装器同口径。

## v0.2.4 (2026-10-01)

- 安装器卫生批次：`bin/install.js` / `install.sh` 统一（未知参数报错 exit 2、`--help` / `--version`、残留清理白名单、嵌套载荷保留）；由模板单一真源渲染，接入漂移门禁。
- 自带安装器测试（`test/install.test.js`）更新为统一行为断言。

## v0.2.3 (2026-09-25)

口径修正：常驻启用改为可选 + 明确关闭通道（ClawHub LLM 复核）。

- SKILL.md「常驻注入（必须，勿跳过）」改为「常驻启用（可选，需用户同意）」：说明不常驻也能手动触发；写入常驻清单 / 系统提示词 / 宿主配置前必须先展示将改动什么并征得同意；用户说「不用元引 / 关掉常驻」立即停止自动介入。
- 安装器加固：拒绝对符号链接目标写入、不做整目录删除；批量安装需 `--yes`。

- `clarify` 未识别输入新增可执行追问契约：3 个问题、3 个候选方向与可复制补充模板；JSON 增加 `questions` / `choices` / `template`。
- 退出码保持 `1`，兼容原有“未识别”判断；新增文本与 JSON 两条回归。

## v0.2.2 (2026-09-17)

## v0.2.1 (2026-09-17)

- 授权边界修复：常驻启用保持不变，但注册永久记忆 / 宿主配置前先征得用户同意；同时把“发给任何 AI”的无主语表述改为“交给任何 AI”，消除装前扫描对数据外传 / 免确认写入的 high 级提示。

## v0.2.0 (2026-09-08)

**评测驱动完善**：新增 FAQ，安装器错误处理与测试补齐。

- 新增 references/faq.md，覆盖候选选择、退出码、离线边界与安装排障。
- 安装器支持 --help、参数校验、统一退出码与人话错误提示。

# 更新日志

## v0.1.1 (2026-08-29)

- 安装方式统一为四方式（对齐发布规范 §3.3.1）：方式一 `npx -y @yottameta/yotta-prompt --agent <name>` / `--dir <dir>`（推荐，走 npm 源）；方式二 `git clone https://github.com/YottaMeta/yotta-prompt.git`；方式三 GitHub Download ZIP；方式四 `bash install.sh --agent/--dir/--list`。移除 `npx skills` 与 `-g` 推荐；中英双 README 安装节同步。
- 版本对齐：package.json / SKILL.md / CHANGELOG / 引擎 VERSION / 测试断言 / README 锚点 = 0.1.1。
- 修复：SKILL.md 安装命令改 `--agent <name>` 合规形式，移除 `npx skills add` 推荐。
- 无功能变更（仅文档与版本同步）。

## v0.1.0 (2026-08-28)

初始发布：

- 定位：元引 —— 意图澄清 + 生态入口（开源分发，专注澄清与引导）。
- 核心机制五步：识别意图 → 2-4 候选方向 → 选一 → 深挖（目标/范围/输出/约束）→ 串联到元阁技能输出可跑提示词。
- 引擎：零依赖（Python 3.8+ 标准库）意图澄清 CLI，十个意图域（dev/analysis/planning/memory/security/logs/learning/writing/quality/general），
  关键词加权 + 技能名锁定（yotta-* / 元X），候选不足自动补「通用引导」。
- map：方向 / 技能名 → 元阁 16 技能（中文名 / 一句话 / 安装命令）+ 可直接运行的提示词模板。
- scenarios：18 个内置场景案例，覆盖任何行业（周报 / 表格 / 学习计划 / 演讲稿 / 翻译 / 会议纪要 / 合同审阅 / 头脑风暴 / 面试准备等；完整示例见 references/scenarios.md）。
- 输出 text / JSON；退出码 0 / 1 / 4。
- 常驻注入：frontmatter always-load + SKILL.md「常驻注入（必须，勿跳过）」双栏声明。
- 自包含提示词（优雅降级）：map / 场景输出为「行为优先」提示词，目标技能未安装也能直接运行；已安装则自动增强；用户一个技能都没装也可直接用。
- 测试：41 个用例全绿；含 CLI 端到端（候选 / map / scenarios / 退出码 / JSON）。
- 文档：SKILL.md + README 中英双版 + references/scenarios.md。
