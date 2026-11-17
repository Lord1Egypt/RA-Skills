## Description:

Wen-Xin is a meta-skill that requires an agent to perform a completion-time self-check before reporting task results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xp1001](https://clawhub.ai/user/xp1001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Wen-Xin to add a completion-time self-review loop that checks requirement coverage, edge cases, and result quality before an agent reports completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can impose broad completion-time workflow guidance across tasks and sessions when installed as a global rule.

Mitigation: Install it only where a persistent self-check is desired, and scope any global-rule configuration to the agents or workspaces that need it.

Risk: The source instructions are primarily written in Chinese, which may not match every user's language or output-format expectations.

Mitigation: Adapt the wording before deployment when the target users need another language or stricter reporting format.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xp1001/skills/wen-xin)
- [Server-resolved source repository](https://github.com/xp1001/wen-xin)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown guidance and checklist text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code; behavior depends on agent adoption of the self-check instructions.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
