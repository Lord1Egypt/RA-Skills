## Description:

AI-powered Xiaohongshu (RED) note compliance auditor that reviews note content for policy compliance, shadowban risk, and optimization suggestions, and requires an API key from wsdsocial.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wsd-mj](https://clawhub.ai/user/wsd-mj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to submit Xiaohongshu (RED) note text for compliance review, shadowban risk assessment, and visibility optimization guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted RED note text is sent to ai.wsdsocial.com for third-party processing.

Mitigation: Do not submit confidential, regulated, client, or otherwise sensitive content unless authorized to share it with that service.

Risk: The skill requires a WSD_API_KEY credential.

Mitigation: Keep the API key out of source control, logs, screenshots, and shared transcripts.

## Reference(s):

- [Server-resolved GitHub provenance: WSD-MJ/red-note-audit](https://github.com/WSD-MJ/red-note-audit)
- [ClawHub skill page: Red Note Audit](https://clawhub.ai/wsd-mj/skills/red-note-audit)
- [WSD Social skill API key page](https://ai.wsdsocial.com/skills)
- [Red Note Audit API endpoint](https://ai.wsdsocial.com/api/pub/skills/red-note-audit/_tool_87)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell command examples and third-party API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WSD_API_KEY and sends submitted note content to ai.wsdsocial.com for processing.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
