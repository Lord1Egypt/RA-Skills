## Description:

Helps agents draft, review, schedule, and publish social content and manage ShapelessAI jobs, standing agents, and Brand Memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[firstclasstree](https://clawhub.ai/user/firstclasstree)

### License/Terms of Use:

MIT-0

## Use Case:

People managing a ShapelessAI social account use this skill to draft and publish posts, run content jobs, and maintain recurring agents and brand guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing or waking a recurring agent can put content on a connected social account.

Mitigation: Confirm the exact action with the user and review the post text and media before publishing or approving.

Risk: Generated posts or media may misstate facts or miss the intended brand voice.

Mitigation: Review generated content before approval and correct Brand Memory when the source guidance is wrong.

Risk: A credential grants access to manage the user's ShapelessAI account.

Mitigation: Connect only when account management is intended; prefer hosted OAuth setup over the API-key fallback.

## Reference(s):

- [ShapelessAI ClawHub release](https://clawhub.ai/firstclasstree/skills/shapeless)
- [ShapelessAI documentation](https://shapelessai.com/docs)
- [ShapelessAI MCP tools](https://shapelessai.com/docs/mcp.md)
- [ShapelessAI hosted MCP setup](https://shapelessai.com/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration]

**Output Format:** [Plain text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include draft posts, job status, media links, and setup instructions.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
