## Description: <br>
Reviews and improves an existing skill's directory structure, logical completeness, and agent compatibility when a user asks to optimize, review, or check a skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linchuncheng](https://clawhub.ai/user/linchuncheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to review skill folders for structure, workflow clarity, logical gaps, and agent portability before release or iteration. It produces a prioritized review report and actionable optimization guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The review-loop mode can modify the target skill folder by creating missing standard subdirectories. <br>
Mitigation: Run the read-only analyze command first, and use review-loop only on a skill folder where creating scripts, references, or assets directories is acceptable. <br>
Risk: Review recommendations may be incomplete or may not match a project's release requirements. <br>
Mitigation: Have a maintainer review the generated report and proposed changes before publishing or deploying the revised skill. <br>


## Reference(s): <br>
- [Structure optimization patterns](references/structure-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown review report with optional shell command suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include prioritized issues, structural summaries, and concrete fix recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
