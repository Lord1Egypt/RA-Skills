## Description:

All-in-one AI video production studio on a visual canvas for generating videos, images, voiceovers, music, lip sync, vocal separation, voice changes, and combined video exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snoopyrain](https://clawhub.ai/user/snoopyrain)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to guide an agent through end-to-end AI video production in VPick, including canvas setup, asset generation, audio production, lip sync, editing, and export. It is suited for users who want one workflow for short films, social clips, narrated videos, and multi-shot AI scenes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP link is a credential and can grant access to the user's VPick account.

Mitigation: Treat the MCP link like a password and avoid sharing it in prompts, logs, screenshots, or public repositories.

Risk: Large or repeated generation jobs may spend VPick credits.

Mitigation: Confirm the user's intent, model choice, duration, and expected cost before running larger generations.

Risk: Prompts and uploaded media are processed by VPick and routed to third-party model providers.

Mitigation: Avoid submitting sensitive, private, or unlicensed media unless the user has confirmed it may be processed by those services.

## Reference(s):

- [VPick MCP connection guide](https://vpick-doc.10xboost.org/guide/mcp-connection.html)
- [VPick app](https://vpick.10xboost.org)
- [ClawHub skill page](https://clawhub.ai/snoopyrain/skills/vpick-video-creator)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration, API calls]

**Output Format:** [Markdown guidance with structured MCP tool parameters and workflow examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference cloud generation outputs, generated media URLs, model choices, and VPick credit usage.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
