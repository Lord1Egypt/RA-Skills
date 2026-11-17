## Description:

Estimates a relative transpiration index for indoor plants from leaf images or video and returns analysis reports or cloud report history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Plant-care users and developers use leaf thermal images or RGB images, optionally with environmental readings, to assess relative transpiration and possible water stress, and to retrieve previous reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plant images, videos, or their URLs are sent to an external LifeEmergence service, and report history is retrieved from the cloud.

Mitigation: Use only media and URLs approved for external processing; review the service's data-handling terms before enabling cloud analysis or history lookup.

Risk: The skill silently creates or reuses an account-linked identity and stores tokens in a local workspace data directory.

Mitigation: Accept the account-linked workflow before installation and restrict access to the workspace data directory and stored credentials.

Risk: Bundled pet-health and generic-analysis remnants can make the plant-analysis scope ambiguous.

Mitigation: Review returned reports against the requested plant context and independently verify consequential care decisions.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/18072937735/skills/smyx-transpiration-rate-estimation-analysis)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured analysis text or JSON, with report links; Markdown table for report history]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may be saved to a local file. The index is relative (0–100%), not a soil-moisture measurement.]

## Skill Version(s):

1.0.14 (source: server-resolved ClawHub release; bundled SKILL.md states 1.0.16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
