# Changelog

## v0.1.4 (2026-11-05)

- 质量门禁与打包文档修正；发布前测试接入。
- 发布门禁批次：发布工作流在 `npm publish` 前执行版本/发布面检查与 `npm test`；测试版本断言改为从 `package.json` 读取；补齐测试脚本。
- 打包与文档：发布包内容、CHANGELOG / README 与交付说明对齐；规则摘要与注册清单同步。

# 更新日志

## v0.1.3 (2026-11-01)

- 安装器 containment：目标根 / 嵌套链接 fail-closed；受管 Hub 链接解析真实目标；精简安装器同口径。

## v0.1.2 (2026-10-01)

- 安装器卫生批次：`bin/install.js` / `install.sh` 统一（未知参数报错 exit 2、`--help` / `--version`、残留清理白名单、嵌套载荷保留）；由模板单一真源渲染，接入漂移门禁。

## v0.1.1 (2026-10-01)

- 文档修正：家族协同 / 边界 / 版权说明中元题的引用改为已发布实际口径（元题 = 按双向细目表从学校自备题库组卷 + 试卷结构校验，不生成题面，题面由题库提供）；同步更新中英 README 与 `references/copyright.md`。
- 行为零变更：内核 / CLI / 退出码 / 门禁契约不变。
- 新增文档契约回归：家族引用不得回退为「规划中 / (planned)」。

## v0.1.0 (2026-09-24)

初始发布：

- 定位：元案 —— 本地、确定性的教案骨架与覆盖校验技能（零依赖，Python 3.8+ 标准库）；不联网、不调用模型、不内置教材与题目原文。
- 输入：课标映射包 JSON（课题 / 知识点 / 重难点 / 易错点 / 课标来源）+ 可选结构配置 JSON（每课时分钟、环节与比例、必填环节、环节关键词）。
- 能力：教案骨架生成（学习目标带来源、重难点与易错点、五环节 + 分钟级时间分配、板书与评价清单）、覆盖检查（`knowledge_missing` / `stage_missing` / `source_missing` / `time_missing` / `minutes_mismatch`）、映射包 list / show / validate。
- 时间分配：最大余数法，各环节分钟合计精确等于「课时 × 每课时分钟」。
- CLI：`plan` / `check` / `map` / `template`；退出码 0 / 1 / 2 / 3 / 4；支持 `--periods`、`--format md|json`、`--out`、`--stdin`、`--gate findings=<n>`。
- 测试：55 项，Python 3.8.20 / 3.11.9 / 3.13.15 全绿；合成样例（完整教案 / 缺口教案）端到端通过。
- 文档：SKILL.md + references（map-format / plan-format / copyright）+ 中英 README + 四方式安装 + banner。
