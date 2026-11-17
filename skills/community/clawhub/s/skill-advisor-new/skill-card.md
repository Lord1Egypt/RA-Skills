## Description:

Recommends the top three matching skills for a user's task by searching local, built-in, SkillHub, and ClawHub sources, then comparing strengths, drawbacks, and fit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiuwu2495](https://clawhub.ai/user/jiuwu2495)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and WorkBuddy users use this skill when they know the task they want to complete but need help choosing an appropriate skill. It returns a ranked recommendation report and can guide installation after the user confirms a choice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Server security evidence flags this release as suspicious because it presents itself as a read-only recommender while also enabling command execution, remote downloads, and local skill persistence during installation flows.

Mitigation: Require explicit user confirmation before any installation, restrict installation paths, pin installer versions, verify sources, and scan downloaded skills before use.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/jiuwu2495/skills/skill-advisor-new)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown recommendation report with ranked skill comparisons and follow-up installation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs a top-three recommendation with fit scores, benefits, drawbacks, source links, author information, and a summary recommendation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
