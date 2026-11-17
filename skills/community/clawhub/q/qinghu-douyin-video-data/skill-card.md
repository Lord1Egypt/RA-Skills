## Description:

Retrieves Douyin video details by link, including author, play count, engagement, title, music, and publication time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Agents serving users who want to look up a Douyin video's play count and other video details from a shared link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install local tooling or use unpinned package upgrades.

Mitigation: Ask before installing; prefer a preinstalled qhkit in a contained environment and avoid unpinned upgrades where possible.

Risk: Account setup may store credentials and steer users to a particular site.

Mitigation: Let users choose and verify the account site, and explicitly approve credential setup before saving a token.

Risk: Video-data requests can incur paid API charges that vary by result volume.

Mitigation: Estimate costs and obtain user approval before paid calls, especially bulk requests.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-douyin-video-data)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise answer with video metrics; table file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports credits spent on paid calls; large results may be delivered as files.]

## Skill Version(s):

0.1.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
