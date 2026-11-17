## Description:

SPC统计过程控制分析；当用户需要对制造业生产过程进行质量监控、过程稳定性评估、异常点识别、多周期数据对比分析时使用

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Manufacturing quality engineers and operations teams use this skill to analyze process data, select an appropriate SPC control chart, detect Nelson rule violations, evaluate process stability, and compare repeated analysis periods.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a shell command with user-supplied input and output file paths.

Mitigation: Review before installing, use only trusted paths, avoid filenames containing shell metacharacters, and prefer structured script invocation instead of interpolated shell commands.

Risk: The analysis script can create or overwrite an HTML report file.

Mitigation: Choose an explicit output location and check for existing files before running the analysis.

Risk: SPC conclusions depend on correctly formatted, time-ordered manufacturing data and appropriate chart selection.

Mitigation: Validate the Excel data format and chart type against the bundled data format and control chart references before acting on results.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/duding-engicool/skill-spc-analysis)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-spc-analysis)
- [Publisher profile](https://clawhub.ai/user/duding-engicool)
- [控制图使用指南](references/control_chart_guide.md)
- [数据格式规范](references/data_format_spec.md)
- [Nelson 8条规则详解](references/nelson_rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown conversation output with shell commands and an HTML report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The analysis script reads Excel input, can print a stdout summary, and creates or overwrites an HTML SPC report containing SVG control charts.]

## Skill Version(s):

0.1.0 (source: server release evidence; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
