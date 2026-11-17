## Description:

Analyze OpenClaw skill ecosystem dependencies, orphan detection, ecosystem health score, impact analysis, and skill relationships.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjipeng977](https://clawhub.ai/user/wangjipeng977)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use Skill Net to inspect an OpenClaw skill ecosystem, trace dependencies, find skills without trigger phrases, estimate delete impact, and generate health reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The analyzer reads local OpenClaw skill definitions and writes generated dependency reports.

Mitigation: Install and run it only when local skill scanning is intended, and review generated reports before sharing ecosystem details.

Risk: Automated installs may include an unused PyYAML requirement.

Mitigation: Remove or pin the dependency before automated installation when dependency minimization is required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangjipeng977/skills/skill-net)
- [Publisher Profile](https://clawhub.ai/user/wangjipeng977)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Console text, Markdown reports, and JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports English, Chinese, bilingual, JSON, and targeted impact-analysis modes.]

## Skill Version(s):

3.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
