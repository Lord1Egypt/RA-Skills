## Description:

Generate AI images of fictional people for marketing creatives with ReelsFarm (GPT Image, Nano Banana, Seedream, FLUX 3), start from reference templates, and edit results in follow-up turns. Needs a ReelsFarm account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mateohysa](https://clawhub.ai/user/mateohysa)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and marketing teams use the skill to generate fictional people for marketing creatives, start from ReelsFarm reference templates, and refine images in follow-up turns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The ReelsFarm API key is sensitive, and prompts or reference images are shared with ReelsFarm.

Mitigation: Keep REELSFARM_API_KEY private and use only prompts and reference images you are comfortable sending to ReelsFarm.

Risk: Image generation spends credits from the user's plan or trial.

Mitigation: Preview with --dry-run, check current credit pricing, and obtain approval for the quoted cost before generation.

## Reference(s):

- [ReelsFarm MCP documentation](https://reelsfarm.com/docs/mcp)
- [ReelsFarm](https://reelsfarm.com)

## Skill Output:

**Output Type(s):** [Images, API Calls, Shell commands, Guidance]

**Output Format:** [ReelsFarm image assets and JSON operation results, with Markdown guidance and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Media is generated remotely; report an asset only after the operation is complete and the response includes its asset ID and URL.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
