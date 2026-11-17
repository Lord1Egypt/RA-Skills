# Changelog

## v0.1.3 (2026-11-05)

- 质量门禁与打包文档修正；发布前测试接入。
- 发布门禁批次：发布工作流在 `npm publish` 前执行版本/发布面检查与 `npm test`；测试版本断言改为从 `package.json` 读取；补齐测试脚本。
- 打包与文档：发布包内容、CHANGELOG / README 与交付说明对齐；规则摘要与注册清单同步。

# 更新日志

## v0.1.2 (2026-11-01)

- 安装器 containment：目标根 / 嵌套链接 fail-closed；受管 Hub 链接解析真实目标；精简安装器同口径。

## v0.1.1 (2026-10-01)

- 安装器卫生批次：`bin/install.js` / `install.sh` 统一（未知参数报错 exit 2、`--help` / `--version`、残留清理白名单、嵌套载荷保留）；由模板单一真源渲染，接入漂移门禁。

## v0.1.0 (2026-09-24)

初始发布：

- 定位：元题 —— 本地、确定性的组卷与试卷校验技能（零依赖，Python 3.8+ 标准库）；不联网、不调用模型、不生成题面、不内置题目原文。
- 输入：题库 JSON（id / 题型 / 分值 / 难度档 / 考点，可选预计作答时间与来源；难度档位可定义 2-5 档）+ 双向细目表 JSON（题型、题量、每题分值、难度配额、分节必考考点、全卷必考考点、总分、限时）+ 试卷 JSON（只记题目 id 引用）。
- 能力：`assemble` 确定性组卷（先满足分节必考考点与全卷覆盖，再按难度配额补足；固定 seed 可复算）、`check` 试卷缺口检查（未知题 / 重复题 / 总分偏差 / 分节缺失与题量偏差 / 题型与分值偏差 / 难度分布偏差 / 考点缺失 / 超出限时 / 分节未标注）、`bank validate` 与 `blueprint validate` 输入校验、`template` 模板生成。
- 确定性：`assemble --seed` 固定随机性，同一题库 + 蓝图 + seed 得到同一份试卷；`check` 无随机性，同一输入同一份缺口清单。
- 证据链：每条缺口带 `code` / `severity` / `message` / `evidence`（题目 id、期望值、实际值、缺失考点），可直接贴进复核记录。
- CLI：`assemble` / `check` / `bank` / `blueprint` / `template`；退出码 0 / 1 / 2 / 3 / 4；支持 `--seed`、`--format md|json`、`--out`、`--gate findings=<n>`。
- 测试：96 项，Python 3.8.20 / 3.11.9 / 3.13.15 全绿；合成样例（22 题题库 + 蓝图 + 缺口试卷）端到端通过；变异测试确认缺口分支可红。
- 文档：SKILL.md + references（bank-format / blueprint-format / report-format / privacy）+ 中英 README + 四方式安装 + banner。
- 边界：不生成或改写题目内容与答案、不预测考后实测难度与区分度、不做学生排名评语与升学预测；题库、蓝图与试卷只在本机流转。
