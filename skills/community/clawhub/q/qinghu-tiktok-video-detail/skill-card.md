## Description:

Queries TikTok video details by video ID in batches of up to 10 and summarizes engagement and commerce data returned by Qinghu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, sellers, and analysts use this skill to look up TikTok video details and assess video engagement or commerce performance from returned data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may install Node and an unpinned qhkit npm package.

Mitigation: Review and approve installation commands and package source before running them.

Risk: A Qinghu token can be stored in persistent configuration, and setup may switch the account to the cn site.

Mitigation: Approve credential storage and site changes explicitly; review the selected account environment.

Risk: Video-detail lookups incur variable credit charges.

Mitigation: Check the current estimate and obtain user consent before paid calls; report actual credits charged.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-tiktok-video-detail)
- [qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Markdown summary with optional tabular file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Up to 10 video IDs per lookup; reports credits spent on paid calls.]

## Skill Version(s):

0.1.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
