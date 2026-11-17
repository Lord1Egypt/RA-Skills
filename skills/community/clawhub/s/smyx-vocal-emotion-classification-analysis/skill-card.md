## Description:

Classifies pet vocalization audio or video into emotion categories with confidence scores and structured report output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

External users, pet-care operators, veterinary staff, and developers can use this skill to analyze dog or cat vocalizations from local media or URLs, return emotion labels and confidence scores, and query prior cloud-hosted reports. Results are for emotional reference only and are not medical, training, or behavior-modification advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends pet media files or media URLs to external services for analysis and report retrieval.

Mitigation: Use only media approved for third-party processing, avoid recordings with sensitive background audio, and review the service terms before deployment.

Risk: Runs may silently create or reuse a local or platform identity and store returned tokens in a workspace SQLite database.

Mitigation: Run the skill in an isolated workspace, restrict filesystem access, and clear or rotate stored credentials after use.

Risk: The security evidence flags dev-host defaults and hidden identity/API-key handling as issues to clarify before routine use.

Mitigation: Confirm production endpoints, credential handling, and account lifecycle behavior before using the skill for regular workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-vocal-emotion-classification-analysis)
- [Publisher profile](https://clawhub.ai/user/smyx-sunjinhui)
- [API documentation](artifact/references/api_doc.md)
- [Skill demo](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown or JSON text with structured classification results, confidence scores, report links, and history tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cloud report export links and historical report lists when requested.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
