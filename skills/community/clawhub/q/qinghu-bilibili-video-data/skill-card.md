## Description:

Retrieves Bilibili video details and engagement metrics from a video link using Qinghu's data service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Agents assisting Bilibili creators and analysts use this skill to look up a video's views, likes, coins, favorites, shares, comments, and other details from its link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Environment setup can install or upgrade qhkit and Node on the host.

Mitigation: Prefer an administrator-managed, pinned qhkit version; approve local tool installations or upgrades before proceeding.

Risk: Configuring a Qinghu API token changes local credentials, and video lookups can incur charges.

Mitigation: Approve credential changes explicitly, review estimated credits, and authorize paid calls before execution.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-bilibili-video-data)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Analysis]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes returned video metrics and reports credits consumed for paid calls.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
