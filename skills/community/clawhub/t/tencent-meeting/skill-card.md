## Description:

Manage Tencent Meeting via REST API to schedule meetings, query meeting details, list cloud recordings, and extract meeting transcripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiayubinx-ux](https://clawhub.ai/user/jiayubinx-ux)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to have an agent create and inspect Tencent Meeting sessions, list cloud recordings, and retrieve meeting transcripts through the Tencent Meeting REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Enterprise Tencent Meeting credentials can be used to create meetings and access recordings or transcripts.

Mitigation: Install only when this access is intended and restrict the required Tencent Meeting API credentials to appropriate users and scopes.

Risk: Recording download URLs and transcript text may expose sensitive meeting content.

Mitigation: Confirm the meeting, user ID, authorization, and sharing destination before retrieving or exposing recordings or transcripts.

## Reference(s):

- [Tencent Meeting API Quick Reference](references/api-guide.md)
- [Tencent Meeting Open API](https://meeting.tencent.com/open-api.html)
- [ClawHub skill page](https://clawhub.ai/jiayubinx-ux/skills/tencent-meeting)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Text, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; command results are JSON or plain text transcripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Tencent Meeting Open API credentials; transcript and record detail operations may require STS-Token.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
