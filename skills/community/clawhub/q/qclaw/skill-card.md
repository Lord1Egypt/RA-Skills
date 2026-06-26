## Description: <br>
Summarize noisy WeChat group chats into decisions, action items, mentions, risks, and tracked keywords for OpenClaw workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ProjectSnowWork](https://clawhub.ai/user/ProjectSnowWork) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, operators, and project teams use QClaw to turn user-provided WeChat group transcripts into concise summaries, decisions, action items, keyword hits, and risk signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WeChat group transcripts can contain personal, client, employee, financial, or confidential details. <br>
Mitigation: Redact unnecessary sensitive details before pasting or exporting chat content into the agent workflow. <br>
Risk: Summaries may omit nuance or be unsuitable where exact records are required. <br>
Mitigation: Avoid using the skill for legal or compliance workflows that require verbatim records. <br>


## Reference(s): <br>
- [QClaw ClawHub skill page](https://clawhub.ai/ProjectSnowWork/qclaw) <br>
- [ProjectSnowWork ClawHub publisher profile](https://clawhub.ai/user/ProjectSnowWork) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown digest with sections for summary, decisions, action items, keyword hits, and risks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill summarizes user-provided chat content and should mark uncertainty rather than fabricate missing context.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
