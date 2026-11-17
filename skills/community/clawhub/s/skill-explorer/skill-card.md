## Description:

Systematically discover, evaluate, compare, and assess OpenClaw skills to find safe, high-quality options for a specific task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[riverfor](https://clawhub.ai/user/riverfor)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to search for OpenClaw skills, compare candidates, inspect quality and safety signals, and prepare recommendations before installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper workflow can force-install unreviewed third-party skills locally before they have been inspected.

Mitigation: Review third-party skills in an isolated environment, avoid the helper script's download action on unknown skills on a main machine, and prefer static unpacking before installation.

## Reference(s):

- [Skill Explorer on ClawHub](https://clawhub.ai/riverfor/skills/skill-explorer)
- [Publisher profile: riverfor](https://clawhub.ai/user/riverfor)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown reports with comparison tables, recommendations, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include security review notes, installation recommendations, and decision-support summaries.]

## Skill Version(s):

1.0.0 (source: release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
