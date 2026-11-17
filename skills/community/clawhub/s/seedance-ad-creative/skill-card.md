## Description:

Generates cinematic product or brand ad clips from a product description or image by preparing a concise creative brief, writing a timestamped Seedance 2.5 prompt, estimating cost, and invoking the Ofox video workflow for submission, polling, download, and cost reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ofoxai](https://clawhub.ai/user/ofoxai)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use this skill to turn product descriptions or product photos into commercial-style brand video clips with guided creative choices, cost awareness, and Ofox API execution. It is suited to product ads, landing-page hero clips, and social ad concepts, not dialogue-driven scenes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product descriptions or images are sent to Ofox for video generation.

Mitigation: Use the skill only with content that is acceptable to share with Ofox, and avoid confidential product material unless the user's policy allows it.

Risk: The skill can trigger paid video generation through an OFOX_API_KEY.

Mitigation: Require a visible dry-run cost table and explicit user approval before any real generation command.

Risk: Recovery or installer commands may change the user's local skill setup.

Mitigation: Have the user review and run installer commands themselves, preferably from a trusted or pinned install path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ofoxai/skills/seedance-ad-creative)
- [ClawHub publisher profile](https://clawhub.ai/user/ofoxai)
- [Skill homepage](https://github.com/ofoxai/skills/tree/main/skills/seedance-ad-creative)
- [Ofox API key setup](https://app.ofox.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with creative brief recap, generated prompt, cost table, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OFOX_API_KEY plus curl and jq; billable generation commands are expected to use an explicit approval flag after cost review.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
