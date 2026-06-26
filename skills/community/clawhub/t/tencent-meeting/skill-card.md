## Description: <br>
Manage Tencent Meeting (腾讯会议) via REST API. Schedule/create meetings, query meeting details, list cloud recordings, and extract meeting transcripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiayubinx-ux](https://clawhub.ai/user/jiayubinx-ux) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and agents use this skill to create Tencent Meeting sessions, query meeting details, retrieve cloud recording metadata, and extract meeting transcripts through Tencent Meeting REST APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Tencent Meeting API credentials and may expose credentials, temporary auth headers, transcript text, or recording URLs through terminal output or logs. <br>
Mitigation: Use scoped, revocable credentials; avoid sharing terminal output; and review logs for sensitive meeting data before retention or disclosure. <br>
Risk: The skill can create meetings and retrieve recordings or transcripts when invoked with broad or ambiguous prompts. <br>
Mitigation: Confirm the intended Tencent Meeting action, meeting identifier, operator identity, and transcript or recording access before running the corresponding command. <br>


## Reference(s): <br>
- [Tencent Meeting API Quick Reference](references/api-guide.md) <br>
- [Tencent Meeting Open API](https://meeting.tencent.com/open-api.html) <br>
- [Tencent Meeting API Base URL](https://api.meeting.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands plus JSON or plain-text API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include meeting metadata, recording download URLs, transcript text, AI summaries, and API error details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
