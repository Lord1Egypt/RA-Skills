## Description:

Fine-tune a reusable brand, style, or character LoRA from a small set of reference images, then generate on-brand imagery from prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runware](https://clawhub.ai/user/runware)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and brand teams use this skill to train a reusable style model from an approved image dataset and then generate consistent brand or character imagery at scale.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Training datasets may contain private or sensitive images and the skill directs agents to host the dataset as a publicly reachable ZIP.

Mitigation: Use only images authorized for third-party training, strip EXIF and location metadata, prefer short-lived signed URLs or approved private upload paths, and delete the archive after ingestion.

## Reference(s):

- [Worked Recipes](references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/runware/skills/train-style-model)

## Skill Output:

**Output Type(s):** [guidance, code, configuration]

**Output Format:** [Markdown guidance with JSON API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes asynchronous training submission, polling, model registration, and post-training image generation guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
