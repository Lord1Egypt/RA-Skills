## Description: <br>
Security guard skill for OpenClaw - Analyzes user input for harmful content, risky commands, and security threats before invoking LLM <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[John-niu-07](https://clawhub.ai/user/John-niu-07) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to screen user input, URLs, files, and video content for harmful content, risky commands, security threats, and prompt injection before invoking an LLM. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided URLs, files, or video content may be sent to configured model providers or optional extraction services. <br>
Mitigation: Avoid processing confidential local files or sensitive links unless the selected provider and service retention policies are acceptable. <br>
Risk: Generated safety judgments may be incorrect or incomplete. <br>
Mitigation: Review safety outputs before relying on them for blocking, enforcement, or deployment decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/John-niu-07/safety-guard-skill-xidian) <br>
- [Publisher profile](https://clawhub.ai/user/John-niu-07) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can emit machine-readable JSON when the documented --json flag is used.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
