## Description:

Make AI product photos and infographics with ReelsFarm: import a product image, place the product in a new scene or a person's hands, or fill a product or infographic template. Needs a ReelsFarm account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mateohysa](https://clawhub.ai/user/mateohysa)

### License/Terms of Use:

MIT-0

## Use Case:

People creating product marketing visuals can use this skill to place product images into scenes or fill product and infographic templates through ReelsFarm. It guides setup, previews, approval, and checking completed media results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media generation spends credits from the user's ReelsFarm plan or trial.

Mitigation: Preview with --dry-run, check current pricing, and get user approval before running a generation.

Risk: The workflow uses an API key and sends selected images to ReelsFarm.

Mitigation: Protect the API key and use only images the user is comfortable sending to ReelsFarm.

Risk: The external CLI implementation and server-side behavior were not audited.

Mitigation: Review the generated action and its cost before confirming execution.

## Reference(s):

- [ReelsFarm MCP documentation](https://reelsfarm.com/docs/mcp)
- [ReelsFarm](https://reelsfarm.com)

## Skill Output:

**Output Type(s):** [Images, Infographics, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Generated image assets and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a ReelsFarm account and API key; media generation uses account credits.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
