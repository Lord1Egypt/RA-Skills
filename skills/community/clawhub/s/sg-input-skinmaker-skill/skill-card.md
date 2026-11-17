## Description:

Generates Sogou Input Method hot-word skin backgrounds from a user-supplied image by composing a guarded image-to-image prompt and returning the generated image with a fixed campaign page link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill inside an AI client to turn an uploaded image and optional style request into a clean horizontal Sogou keyboard-skin background. Developers and agent operators can use it as a workflow skill for guarded prompt assembly around image-to-image generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill returns a fixed Chinese contest/prize message and external Sogou H5 campaign link that may become stale or unsuitable outside the campaign context.

Mitigation: Verify that the campaign claim and link are current and appropriate for the intended users before release or deployment.

## Reference(s):

- [Generation Prompt Reference](references/generation-prompt.md)
- [ClawHub Skill Page](https://clawhub.ai/tencent-adm/skills/sg-input-skinmaker-skill)
- [Sogou Campaign Page](https://pinyin.sginput.qq.com/h5/kaixueskill/share/225448950305128448)

## Skill Output:

**Output Type(s):** [Guidance, Text, Image]

**Output Format:** [Generated image with concise Markdown text and a fixed URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires one user-provided image; optional style text is rewritten against the skill's image-generation guardrails before use.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
