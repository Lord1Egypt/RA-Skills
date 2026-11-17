## Description:

质量管理QC手法辅助工具；支持柏拉图、鱼骨图、直方图、控制图、散布图等图表自动生成；用户需进行质量分析、问题诊断或数据可视化时使用；覆盖QC七大手法

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Quality managers, manufacturing engineers, and analysts use this skill to generate common QC charts, interpret quality data, diagnose root causes, and prepare visual outputs for quality review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Template loading can read JSON files outside the intended template folder when untrusted template names include path traversal.

Mitigation: Use only trusted template names, reject names containing path separators or '..', and review template mode before deployment.

Risk: The chart generator writes chart and optional analysis files to caller-provided output paths.

Mitigation: Use explicit trusted output directories and review output paths before execution.

Risk: Runtime dependencies can affect execution behavior if installed from an untrusted or unpinned environment.

Mitigation: Install matplotlib, numpy, and pandas from a trusted pinned environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-qc-tools)
- [Publisher profile](https://clawhub.ai/user/duding-engicool)
- [Server-resolved GitHub provenance](https://github.com/duding-engicool/skill-qc-tools)
- [QC手法操作指南](references/qc_guide.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, files]

**Output Format:** [Markdown guidance with shell commands plus generated chart files and optional JSON analysis output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Pareto, fishbone, histogram, control, and scatter chart workflows with user-provided JSON data or named templates.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
