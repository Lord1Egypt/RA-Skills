## Description:

Multi-model AI image generation on a visual canvas with support for text-to-image, image-to-image, style transfer, multi-reference composition, batch generation, and aspect ratio control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snoopyrain](https://clawhub.ai/user/snoopyrain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate and manage AI images through a VPick visual canvas, including artwork, illustrations, character references, style transfer, and batch variants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP URL contains an embedded authentication token that grants generation access to the user's VPick account.

Mitigation: Treat the MCP URL as a password, do not share it publicly, and regenerate it from VPick settings if exposure is suspected.

Risk: Prompts and uploaded reference images are sent through VPick and routed to third-party model providers for processing.

Mitigation: Avoid sending sensitive prompts or private reference images unless that data flow is intended and acceptable.

Risk: Image generations can consume the user's VPick credit balance.

Mitigation: Review model pricing and monitor usage before running batch or high-resolution generations.

## Reference(s):

- [VPick MCP connection guide](https://vpick-doc.10xboost.org/guide/mcp-connection.html)
- [VPick application](https://vpick.10xboost.org)
- [ClawHub skill page](https://clawhub.ai/snoopyrain/skills/vpick-ai-image-generator)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text, Markdown]

**Output Format:** [Markdown with tool-call examples and concise procedural guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger VPick image generations that create stored image files and spend account credits.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
