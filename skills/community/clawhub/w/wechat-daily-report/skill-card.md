## Description: <br>
Generates mobile-resolution PNG daily report images from WeChat group chat exports by combining chat statistics with AI-generated summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justao](https://clawhub.ai/user/justao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
People analyzing WeChat group chats use this skill to turn authorized chat export JSON into statistics, AI-written summaries, and a phone-sized PNG daily report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can expose private WeChat chat text, names, secrets, or sensitive messages during AI analysis. <br>
Mitigation: Use only chat exports you are authorized to process, redact sensitive content before analysis, prefer a local or approved AI provider, and delete generated chat-text and report artifacts when no longer needed. <br>
Risk: The server security verdict marks this release suspicious and recommends review before installation. <br>
Mitigation: Review the artifact and generated outputs before deployment, and scan the skill in the target environment before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justao/wechat-daily-report) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Text, JSON, Files] <br>
**Output Format:** [Markdown instructions with bash commands; generated artifacts include JSON, text, and PNG image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Final report output is a mobile-resolution PNG long image; intermediate files include stats.json, simplified_chat.txt, and ai_content.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
