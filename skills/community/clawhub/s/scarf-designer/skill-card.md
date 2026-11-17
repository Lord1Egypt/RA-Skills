## Description:

Helps create custom scarf designs for print-on-demand and manufacturing using prompts, garment options, reference images, and personalized text or logos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Designers and makers use this skill to request personalized scarf concepts and view generated design assets through a shared workspace. A DeepNLP OneKey access key is required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Garment prompts, reference image URLs, customization details, tags, and session names are sent to the DeepNLP/Craftsman service using an API key.

Mitigation: Share only design data appropriate for that service; avoid proprietary or regulated material unless the service is trusted, and protect the API key.

Risk: Generated workspace share links may expose design work to anyone who receives them.

Mitigation: Treat share links as sensitive and share them only with intended recipients.

Risk: The example CLI invokes an unpinned npx package.

Mitigation: Prefer trusted, version-pinned CLI tooling before running the example.

## Reference(s):

- [Scarf Designer release](https://clawhub.ai/ai-hub-admin/skills/scarf-designer)
- [Craftsman scarf designer](https://craftsman-agent.aiagenta2z.com/app/clothing-designer/scarf)
- [DeepNLP OneKey access keys](https://www.deepnlp.org/workspace/keys)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with JSON API examples and generated-workspace links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The design service may provide preview images, design data, and a shared workspace URL.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
