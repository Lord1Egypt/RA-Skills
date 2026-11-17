## Description:

生成项目流程可视化图表，支持乌龟图(5M1E)、泳道图、流程图和时间线模板，用于绘制项目流程图、过程乌龟图或导出流程可视化结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, quality engineers, and process analysts use this skill to convert structured process descriptions into SVG or PNG workflow diagrams. It is suited for quality-management process documentation, 5M1E turtle diagrams, swimlane diagrams, standard flowcharts, and timelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SVG files can include unescaped user-provided diagram text.

Mitigation: Use trusted diagram content only, review generated SVG before use, and avoid opening SVGs from untrusted inputs in privileged browser contexts.

Risk: The diagram script can write output paths too broadly.

Mitigation: Write outputs only to explicit safe filenames in a controlled directory and constrain output paths before broad deployment.

Risk: The security verdict is suspicious.

Mitigation: Review before installing and scan the skill before deployment.

## Reference(s):

- [GitHub repository](https://github.com/duding-engicool/skill-process-turtle)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-process-turtle)
- [ClawHub publisher profile](https://clawhub.ai/user/duding-engicool)
- [Template reference](references/templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell commands that produce SVG or PNG files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill prepares diagram configuration and invokes a local script that reports generated SVG and optional PNG paths.]

## Skill Version(s):

0.1.0 (source: release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
