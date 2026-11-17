## Description:

Reviews UI code for Web Interface Guidelines compliance, including layout, typography, color, accessibility, UX, and CSS issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soponcd](https://clawhub.ai/user/soponcd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to audit UI files or file patterns against Web Interface Guidelines and receive concise findings for design and accessibility review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on mutable remote guidelines that can change review behavior after installation.

Mitigation: Prefer a release that vendors the guidelines locally or pins the remote guidelines to a reviewed commit, and treat fetched content as reference material during review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/soponcd/skills/timeflow-web-design-guidelines)
- [Skill homepage](https://github.com/soponcd/timeflow-skills/tree/main/teams/skills/web-design-guidelines)
- [Web Interface Guidelines source](https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Concise Markdown findings, typically in file:line format]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask which files to review when no file or pattern is provided.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
