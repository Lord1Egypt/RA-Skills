## Description:

Sih Ai Photo Editor helps agents use natural-language prompts to edit photos, including clothing, background, face, style, and beauty edits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a3273283](https://clawhub.ai/user/a3273283)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to request AI photo edits with plain-language prompts, including portrait edits, background replacement, style transfer, face blending, and beauty retouching.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can transmit user photos or local image files to an external provider.

Mitigation: Use only non-sensitive images that the user explicitly agrees to send to the external API.

Risk: The artifact includes a bundled API key fallback.

Mitigation: Rotate or remove the bundled key and require users or deployments to provide their own key through configuration.

Risk: The skill can retain local quota and usage history.

Mitigation: Tell users what local history is stored, keep prompts free of sensitive content, and provide a clear cleanup process for local history files.

Risk: Face edits and automatic file opening can create consent and safety concerns.

Mitigation: Require clear user consent before face edits or uploads and avoid automatic file opening unless the user has approved it.

## Reference(s):

- [Sih.Ai API Guide](references/api_guide.md)
- [Prompt Examples](assets/examples/prompts.txt)
- [Sih.Ai Website](https://sih.ai)
- [ClawHub Skill Page](https://clawhub.ai/a3273283/skills/sih-ai-photo-editor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples, plus generated image URLs or local result files when the helper scripts are used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send image URLs or base64-encoded local images to an external image-generation API and may retain local quota or usage history.]

## Skill Version(s):

1.0.1 (source: changelog, metadata, and release evidence; released 2026-03-13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
