## Description:

QVeris helps agents discover specialized API tools by capability and call selected tools for structured data, media, document, translation, and other external workflows using QVERIS_API_KEY.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linfangw](https://clawhub.ai/user/linfangw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to find API tools by capability, evaluate candidates, and call selected QVeris-backed tools for structured data or external processing tasks. It is suited for workflows that need tool discovery before execution rather than direct factual answering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Relevant task details and tool-call parameters are sent to QVeris under the configured API key.

Mitigation: Use the skill only when that data sharing is acceptable under the applicable QVeris account and data handling expectations.

Risk: Secrets or sensitive personal, medical, financial, or proprietary data could be included in discovery queries or tool parameters.

Mitigation: Avoid sending sensitive data unless the specific use is approved for the QVeris account and workflow.

Risk: Discovery identifies API tools by capability and does not directly answer factual questions.

Mitigation: Use QVeris discovery for tool selection, then call the selected tool or use web search for factual and qualitative information needs.

## Reference(s):

- [QVeris Homepage](https://qveris.ai)
- [ClawHub Skill Page](https://clawhub.ai/linfangw/skills/qveris-test)
- [ClawHub Publisher Profile](https://clawhub.ai/user/linfangw)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires QVERIS_API_KEY and sends QVeris discovery queries and tool-call parameters to qveris.ai.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
