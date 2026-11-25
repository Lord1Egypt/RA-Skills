# 端到端工作流示例

## 1. 一次快速开始

```bash
python scripts/yotta_resume.py quickstart --resume resume.md --jd jd.txt \
  --out-dir yotta-resume-action-pack
```

先确认自检 PASS，再阅读分析报告、表达清晰度追问和用户级下一步。
需要 JSON 时追加 `--format json`；行动包包含 `action-plan.md`、
`audit-report.md` 和 `action-pack.json`。

## 2. 安装后自检

```bash
python scripts/yotta_resume.py selftest --quick
python scripts/yotta_resume.py selftest --full --json
```

自检不读取用户简历。`WARN` 只影响可选能力，`FAIL` 时停止并修复。

## 3. 分析

```bash
python scripts/yotta_resume.py audit --resume resume.md --jd jd.txt --format json
```

读取 `source_manifest`、`parse_warnings`、`industry_detection`、`issues`、
`questions`、`unknowns` 和 `jd_match`。先确认行业、输入质量和事实边界，再改简历。

## 4. 追问与确认

按问题的优先级向用户确认：

1. 个人责任：主导、共同负责、协助还是参与。
2. 规模：系统数、告警量、时间窗、覆盖团队。
3. 方法：工具、流程、验证和回滚。
4. 结果：可证明的基线、变化和证据。

未确认的事实不写入简历。

## 5. 修改 Markdown

```markdown
### 示例科技 | 安全运营工程师 | 2023.01 - 2026.01
- 负责 6 个业务系统的 SIEM 规则维护，按周复盘 100 条脱敏样本，未公开真实告警数据。
```

## 6. 事务化导出

```bash
python scripts/yotta_resume.py export --input revised.md --docx revised.docx --html revised.html --pdf revised.pdf
```

全部格式成功后才会写入目标路径。任一格式失败时保留原有文件，不留下本次半成品。

## 7. 单轮模拟面试

```bash
python scripts/yotta_resume.py interview start \
  --resume resume.md --jd jd.txt --role-family soc --level mid \
  --session interview-session.json
```

把当前问题回答写入临时 Markdown 文件，再执行：

```bash
python scripts/yotta_resume.py interview answer \
  --session interview-session.json --answer answer.md
```

证据不足时工具会返回一次题库追问；回答后自动进入下一题。全部主题完成后运行：

```bash
python scripts/yotta_resume.py interview review \
  --session interview-session.json --format markdown
```

复盘只展示证据状态、缺口、简历改写方向和来源化学习重点，不生成主观分数。

非安全行业可省略 `--role-family`，工具会自动映射对应岗位族：

```bash
python scripts/yotta_resume.py interview start \
  --resume software.md --session software-session.json
```

## 8. 交付检查

- 核对 `selftest`、行动包、目标和实际文件名。
- DOCX / PDF 必须可打开，PDF 应包含文字层。
- 报告联系方式已打码，成品按用户确认保留。
- 模拟面试会话只在用户显式指定的文件中保存；不需要时直接删除该文件。
- 不承诺 ATS、面试或 Offer 结果。

## 9. 离线边界

分析、模拟面试、导出、`selftest`、`doctor`、`contracts` 和行动包生成只读取本地文件。
发布包不包含来源抓取或题库维护命令。
