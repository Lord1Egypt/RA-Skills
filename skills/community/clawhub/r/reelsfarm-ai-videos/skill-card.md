## Description:

Generate short AI videos for ReelsFarm account holders from a prompt, start and end frames, or reference images (Seedance, Veo, Gemini Omni), and turn an avatar image into a hook clip that opens with a reaction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mateohysa](https://clawhub.ai/user/mateohysa)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and social media teams use this skill to generate short videos from prompts, frames, or reference media, and to animate ReelsFarm avatars into hook clips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generating media spends credits from the user's ReelsFarm plan or trial.

Mitigation: Preview each action, check its credit price, and get approval for the cost before running it.

Risk: The ReelsFarm API key can expose account access if disclosed.

Mitigation: Keep REELSFARM_API_KEY private and store it securely.

Risk: Submitted prompts and media are processed through ReelsFarm.

Mitigation: Use only media you are comfortable processing through the service.

Risk: The external CLI implementation and referenced companion skills were not reviewed.

Mitigation: Review their behavior and permissions before use.

Risk: Generated clips could depict a real identifiable person without consent or present an AI person as a real customer.

Mitigation: Get consent before depicting identifiable people and clearly avoid presenting AI people as real customers.

## Reference(s):

- [ReelsFarm MCP documentation](https://reelsfarm.com/docs/mcp)
- [ReelsFarm](https://reelsfarm.com)
- [ClawHub skill page](https://clawhub.ai/mateohysa/skills/reelsfarm-ai-videos)

## Skill Output:

**Output Type(s):** [Video assets, Hook clips, JSON status and result information]

**Output Format:** [ReelsFarm-hosted media assets with JSON job status and asset details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video jobs run asynchronously and one job runs at a time per account; a completed status with an asset ID and URL confirms creation.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
