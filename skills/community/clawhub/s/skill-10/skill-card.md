## Description:

Edit Clawra's reference image with Grok Imagine (xAI Aurora) and send selfies to messaging channels via OpenClaw

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangzhi8145](https://clawhub.ai/user/wangzhi8145)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to generate edited Clawra selfie images from user-provided context and send them to selected messaging channels through OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can generate images through a third-party provider and send them to real messaging channels.

Mitigation: Use it only with OpenClaw scoped to approved channels and require explicit confirmation before dispatch.

Risk: The example TypeScript implementation shells out with interpolated values.

Mitigation: Avoid that example as written; pass arguments without a shell before using similar code.

Risk: The release is marked suspicious because it grants broad messaging and command authority with insufficient safeguards.

Mitigation: Review the skill before installation and limit credentials and channel access to the minimum needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangzhi8145/skills/skill-10)
- [Clawra reference image](https://cdn.jsdelivr.net/gh/SumeLabs/clawra@main/assets/clawra.png)
- [fal.ai dashboard keys](https://fal.ai/dashboard/keys)
- [Grok Imagine edit API endpoint](https://fal.run/xai/grok-imagine-image/edit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces image-generation and message-sending guidance that depends on FAL_KEY and OpenClaw gateway credentials.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
