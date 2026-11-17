## Description:

Generates realistic, dialogue-driven short-drama video clips from a script or scene description using the Ofox video API and Seedance 2.5.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ofoxai](https://clawhub.ai/user/ofoxai)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, developers, and agent users use this skill to turn a dialogue beat or scene description into a short, realistic video clip with prompt structure, cost review, submission, polling, download, and cost reporting guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends scripts, dialogue, prompt details, and generated-job metadata to Ofox.

Mitigation: Use it only when that external API processing is acceptable, and avoid submitting sensitive material unless policy permits it.

Risk: The skill can initiate paid video-generation jobs after approval.

Mitigation: Review the displayed cost table before approving a run and use a trusted, current ofox-video-core dependency that enforces quote-first approval.

Risk: The skill requires an Ofox API key.

Mitigation: Provide the key through the environment and avoid pasting it into prompts, generated scripts, or logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ofoxai/skills/seedance-short-drama)
- [Declared homepage](https://github.com/ofoxai/skills/tree/main/skills/seedance-short-drama)
- [Ofox API key console](https://app.ofox.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with structured prompt text, cost tables, and bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OFOX_API_KEY and local curl and jq; paid runs require explicit cost approval before submission.]

## Skill Version(s):

2.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
