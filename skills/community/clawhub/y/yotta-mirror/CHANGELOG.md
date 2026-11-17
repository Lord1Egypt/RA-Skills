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

- 定位：元镜 —— 本地、确定性的学情分析技能（零依赖，Python 3.8+ 标准库）；学生数据不出本机。
- 输入：成绩 / 答题表（CSV / TSV / 标准输入）+ 题目-知识点映射 JSON + 可选阈值配置 JSON。
- 内核：数据闸门（列/行一致性、重复学生、非数值、分值越界）、逐题统计（作答/缺失/平均分/得分率/满分/零分）、按分值加权的知识点掌握率、学生 A/B/C 分层与临界生识别、薄弱点诊断（高中低置信分级）、人工复核清单、Markdown + JSON 报告。
- 阈值可配置：`mastery.weak_below` / `mastery.solid_at_or_above` / `layers.a_at_or_above` / `layers.b_at_or_above` / `min_respondents` / `critical_margin`，并随报告回写。
- CLI：`analyze` / `template` / `config validate`；退出码 0 / 1 / 2 / 3 / 4；支持 `--stdin`、`--format json`、`--out`、`--anonymize`、`--gate weak=<n>`。
- 隐私：核心路径零网络、零模型调用；`--anonymize` 用可复算代号替换学生标识；报告固定免责声明（不用于评价、排名、升学判断）。
- 测试：81 项，Python 3.8.20 / 3.11.9 / 3.13.15 全绿；合成样例（薄弱班 / 均衡班）端到端通过。
- 文档：SKILL.md + references（data-format / report-format / privacy）+ 中英 README + 四方式安装 + banner。
