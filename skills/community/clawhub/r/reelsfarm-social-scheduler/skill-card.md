## Description:

Schedule or publish approved ReelsFarm slideshows and videos to your own connected TikTok, Instagram, YouTube and Facebook accounts, with caption checks, per-platform settings from preflight, and best posting times. Needs a ReelsFarm account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mateohysa](https://clawhub.ai/user/mateohysa)

### License/Terms of Use:

MIT-0

## Use Case:

People managing their own connected social accounts can use this skill to review, schedule, and publish approved ReelsFarm content across TikTok, Instagram, YouTube, and Facebook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An exposed ReelsFarm API key could allow access to the connected account and service actions.

Mitigation: Keep REELSFARM_API_KEY private and approve the account, content, caption, privacy settings, and posting time before each action.

Risk: A publishing or scheduling action could post content to the wrong account or with unintended settings or timing.

Mitigation: Preview the action and its cost, inspect preflight settings, and give explicit approval for each individual post; require approval before cancellation.

## Reference(s):

- [ReelsFarm MCP documentation](https://reelsfarm.com/docs/mcp)
- [ReelsFarm](https://reelsfarm.com)
- [ClawHub skill release](https://clawhub.ai/mateohysa/skills/reelsfarm-social-scheduler)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions use the selected account, content, caption, platform settings, and posting time.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
