## Description:

Analyzes reptile photos or videos to estimate shedding stage from visible body and eye changes and return a structured report with care suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Reptile keepers can use enclosure images or videos to monitor apparent shedding progress, review care prompts, and retrieve prior analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports unclear account and credential handling, including risky credential transmission.

Mitigation: Review how credentials are obtained and sent, and use only a minimally privileged test account until the flow is understood.

Risk: The security assessment reports remote media uploads without clear disclosure.

Mitigation: Confirm the upload destination, retention, and access controls, and obtain consent before submitting enclosure images or videos.

Risk: The security assessment says the export-only option may still run analysis.

Mitigation: Verify the option's behavior before relying on it to avoid analysis or remote processing.

Risk: The security scan is incomplete because a local reference was missing.

Mitigation: Review the missing referenced material before deployment.

## Reference(s):

- [API reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-reptile-shedding-progress-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Text, Markdown]

**Output Format:** [Structured JSON report with a text heading and report link; history results are JSON suitable for a Markdown table.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include visual shedding-stage estimates, care suggestions, risk prompts, and report links.]

## Skill Version(s):

1.0.18 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
