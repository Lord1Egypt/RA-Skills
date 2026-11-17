## Description:

Generates clean catalog-style e-commerce product video prompts and Ofox video-generation commands from a product photo or product description, including a creative brief, cost estimate, submission, polling, download, and final cost reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ofoxai](https://clawhub.ai/user/ofoxai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn product photos or text descriptions into listing-ready product video workflows through Ofox and Seedance 2.5. It is intended for clean catalog and marketplace showcase clips, not cinematic advertising or people/dialogue workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product images, prompts, and job data are sent to Ofox during generation.

Mitigation: Use the skill only with data suitable for Ofox processing and confirm that the user is comfortable with that transfer before running generation commands.

Risk: The workflow can create paid generation jobs.

Mitigation: Show the dry-run cost estimate first, wait for explicit approval, and use real-run commands only with the approval flag required by ofox-video-core 2.0.0 or newer.

Risk: Untrusted or outdated core tooling could change billing or request behavior.

Mitigation: Install or update ofox-video-core only from a trusted source and require version 2.0.0 or newer.

Risk: The skill is not intended for people or dialogue workflows.

Mitigation: Route requests involving people, presenters, or dialogue to a more appropriate skill instead of using this product-video workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ofoxai/skills/seedance-product-video)
- [Metadata homepage](https://github.com/ofoxai/skills/tree/main/skills/seedance-product-video)
- [Ofox API keys](https://app.ofox.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated prompt text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OFOX_API_KEY, curl, jq, and ofox-video-core 2.0.0 or newer for paid generation workflows.]

## Skill Version(s):

2.0.0 (source: server release evidence, artifact frontmatter, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
