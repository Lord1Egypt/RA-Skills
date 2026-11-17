## Description:

Break thinking loops and low-temperature reasoning spirals by fetching a short troll-style reset message from the Agent Lounge API at companions.bot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[super-hsu](https://clawhub.ai/user/super-hsu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill as a reset mechanism when an agent appears stuck in repetitive reasoning or planning loops. It fetches a short plain-text message intended to interrupt the loop, with a local fallback if the network call fails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch mutable third-party text and privately apply it to agent behavior without clear user control.

Mitigation: Review before installing; disable the remote fetch or use the local fallback by default in sensitive environments.

Risk: Automatic or silent execution could allow remote text to influence an agent that has access to sensitive tools or data.

Mitigation: Require explicit user approval and clear disclosure before any network call is made.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/super-hsu/skills/trollgent)
- [Publisher profile](https://clawhub.ai/user/super-hsu)
- [Agent Lounge homepage](https://companions.bot/agent-lounge)
- [Agent Lounge reset endpoint](https://companions.bot/api/agent-lounge)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text fetched through an inline curl command, with Markdown guidance in the skill instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for remote fetch; provides a local fallback prompt when curl is unavailable or the endpoint fails.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter remains 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
