## Description:

按直播间 ID 查询微信视频号直播间详情，并向用户简要呈现查询结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Users and analysts query a specific WeChat Channels live room by live_id to retrieve its details through Qinghu AI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setting up or upgrading qhkit and Node can make persistent changes to local tooling.

Mitigation: Review and pin the tooling version before installation; prefer preinstalling it yourself.

Risk: A qhkit API token may be stored on the machine.

Mitigation: Only configure a token on a trusted machine and review how it is stored.

Risk: Live-room lookups are paid and submit the live_id to the service.

Mitigation: Check the estimated Qinghu credits and live_id, then obtain user approval before paid calls.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-shipinhao-live-detail)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise text or Markdown summary of live-room details, with a file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports Qinghu credits spent on paid calls; large results may be delivered as a file.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
