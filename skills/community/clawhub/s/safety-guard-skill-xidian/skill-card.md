## Description:

Security guard skill for OpenClaw - Analyzes user input for harmful content, risky commands, and security threats before invoking LLM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[john-niu-07](https://clawhub.ai/user/john-niu-07)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to add a safety-analysis step that reviews prompts, URLs, files, or transcripts for harmful content, risky commands, and prompt-injection concerns before invoking a model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Analyzed URLs, documents, transcripts, or extracted content may be sent to the selected model provider and to enabled Firecrawl or Apify fallback services.

Mitigation: Confirm provider and fallback-service data handling before use, avoid sending sensitive content unless approved, and disable optional fallback services when they are not needed.

Risk: Runtime behavior depends on the installed safety-guard executable and Python dependencies.

Mitigation: Review the executable source before deployment and prefer pinned dependency versions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/john-niu-07/skills/safety-guard-skill-xidian)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON safety-analysis output, with Markdown documentation for commands and configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports output length controls and maximum output token settings; URL and YouTube extraction may use optional fallback services when configured.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
