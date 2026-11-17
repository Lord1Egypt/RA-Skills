## Description:

Generates a mobile-resolution PNG daily report from WeChat group chat logs by analyzing chat statistics and AI-generated summary content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justao](https://clawhub.ai/user/justao)

### License/Terms of Use:


## Use Case:

Developers and operators with authorized WeChat group chat exports use this skill to analyze message activity, prepare AI summary content, and generate a daily PNG report for mobile viewing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles full private WeChat group chat text, which may include personal or sensitive content.

Mitigation: Use only authorized chat exports, redact sensitive names or messages before processing, and control access to intermediate text, JSON, and PNG report outputs.

Risk: The security evidence flags the release as suspicious because localized metadata is misleading and expected scripts or prompt sources are missing from the artifact.

Mitigation: Review the skill before installation, run it in an isolated environment, and verify the required scripts and prompt source before following install or execution commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justao/skills/wechat-daily-report)
- [ClawHub publisher profile](https://clawhub.ai/user/justao)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, Files]

**Output Format:** [Markdown guidance with bash commands, JSON intermediate data, and a PNG report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The described workflow produces stats.json, simplified_chat.txt, ai_content.json, and a mobile-resolution PNG report.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
