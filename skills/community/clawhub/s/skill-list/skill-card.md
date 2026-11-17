## Description:

Lists OpenClaw skills in Chinese, including descriptions, functional categories, overlapping capabilities, recommendations, and command-line usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[damiencronw](https://clawhub.ai/user/damiencronw)

### License/Terms of Use:


## Use Case:

OpenClaw users and developers use this skill to inspect locally installed skills, understand their purposes, and identify overlapping functionality before choosing or maintaining skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented duplicate-skill detection, table output, and --category behavior are not fully implemented in the bundled script.

Mitigation: Review script output before relying on categorization or duplicate analysis; treat those sections as guidance unless implementation is completed.

Risk: The script invokes the local ClawHub CLI to list installed skills.

Mitigation: Run it only in an environment where the ClawHub CLI is installed and trusted, and review command output before acting on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/damiencronw/skills/skill-list)
- [ClawHub publisher profile](https://clawhub.ai/user/damiencronw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown and terminal text with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language content; script output depends on locally installed OpenClaw skills and the ClawHub CLI.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
