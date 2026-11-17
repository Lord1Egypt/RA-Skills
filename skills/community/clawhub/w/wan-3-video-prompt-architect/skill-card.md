## Description:

Build and review production-ready prompts and short shot plans for WAN-30.video text-to-video or image-to-video work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gpt-img-2](https://clawhub.ai/user/gpt-img-2)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, and developers use this skill to turn video ideas into inspectable WAN-30.video prompts, short timed shot plans, reference-image roles, configuration notes, assumptions, and preflight warnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional MCP setup tells users to run unpinned remote GitHub code locally.

Mitigation: Review the GitHub repository and dependency tree first, prefer a pinned commit or verified release, and run it with limited filesystem, environment, credential, and network access.

Risk: The skill is primarily prompt-writing guidance, but generated prompts or configuration advice can be incorrect for the live WAN-30.video interface.

Mitigation: Recheck live duration, resolution, image-count, pricing, and policy limits before generation, and keep preflight warnings visible to the user.

Risk: Users may only need prompt drafting and not local MCP execution.

Mitigation: Remove or avoid the MCP configuration when the optional server is not needed.

## Reference(s):

- [WAN-30.video Wan 3.0 Guide](https://wan-30.video/wan-3-0)
- [WAN-30.video Text-to-Video](https://wan-30.video/text-to-video)
- [WAN-30.video Image-to-Video](https://wan-30.video/image-to-video)
- [WAN-30.video Pricing](https://wan-30.video/pricing)
- [Raw Skill](https://wan-30.video/skills/wan-3-video-prompt-architect/SKILL.md)
- [ClawHub Listing](https://clawhub.ai/gpt-img-2/skills/wan-3-video-prompt-architect)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with structured prompt text, shot plans, configuration notes, assumptions, preflight warnings, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not call a model provider, access an account, or spend credits; optional MCP setup is separate from prompt drafting.]

## Skill Version(s):

1.0.0 (source: release evidence and openclaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
