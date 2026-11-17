## Description:

投票鸭助手 helps agents search Toupiaoya voting templates, create text, image, and video voting projects, upload materials, and inspect project, vote, view, option, and group data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eqxiu](https://clawhub.ai/user/eqxiu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create and manage Toupiaoya online voting campaigns, including template search, project creation, material uploads, voting data review, access trend analysis, option management, and group management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a login token locally and can send that token to configurable API endpoints without host validation.

Mitigation: Use the skill only with trusted Toupiaoya endpoints; do not set TOUPIAOYA_API_BASE, EQXIU_AIGC_API_BASE, or --base-url unless you control the endpoint.

Risk: The skill can upload media and submit voting project content to external services.

Mitigation: Do not upload or submit confidential, regulated, or private voting content through this workflow.

Risk: The security verdict recommends review before installation.

Mitigation: Review the skill before use and run it in an isolated Python environment with pinned dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eqxiu/skills/toupiaoya-skill)
- [Publisher profile](https://clawhub.ai/user/eqxiu)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON CLI/API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write an X-Openclaw-Token to the local Toupiaoya configuration file and may upload user-provided media to Tencent Cloud COS through the Toupiaoya workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
