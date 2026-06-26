## Description: <br>
Security guard skill for OpenClaw that analyzes user input for harmful content, risky commands, and security threats before invoking an LLM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[John-niu-07](https://clawhub.ai/user/John-niu-07) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to screen prompts, URLs, files, and command-like requests for harmful content, risky commands, security threats, and prompt injection before invoking an LLM. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports mismatched metadata and unclear third-party data handling. <br>
Mitigation: Review the publisher, the actual CLI implementation, and the metadata mismatch before installing or using the skill. <br>
Risk: Inputs may be sent to configured model or extraction providers. <br>
Mitigation: Avoid sensitive inputs unless the configured providers and optional extraction services are approved for that data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/John-niu-07/safety-guard-skill) <br>
- [Publisher profile](https://clawhub.ai/user/John-niu-07) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Text by default, JSON when requested, with shell command examples and configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports output length controls, maximum output token controls, extract-only mode for URLs, and optional extraction provider fallbacks.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
