## Description:

Security guard skill for OpenClaw - Analyzes user input for harmful content, risky commands, and security threats before invoking LLM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[john-niu-07](https://clawhub.ai/user/john-niu-07)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to check submitted text, URLs, PDFs, YouTube-derived content, and extracted page content for harmful content, risky commands, security threats, and prompt injection before invoking an LLM.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted text, URLs, PDFs, YouTube-derived content, and extracted page content may be sent to the configured model provider or optional Firecrawl and Apify services.

Mitigation: Avoid sensitive local documents and internal URLs unless provider policies and configuration have been reviewed.

Risk: Automated installation may install PyYAML without an explicit version pin.

Mitigation: Pin PyYAML to an approved version before automated installs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/john-niu-07/skills/safety-guard-skill)
- [Publisher profile](https://clawhub.ai/user/john-niu-07)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [Text or JSON safety analysis, depending on invocation flags.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports configurable analysis length and maximum output tokens.]

## Skill Version(s):

1.0.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
