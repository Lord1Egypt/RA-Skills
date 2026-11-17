## Description:

Suggests triage levels (Emergency, Urgent, Outpatient) from symptom descriptions using rule-based red flag matching for AI-assisted decision support, not professional diagnosis.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to produce a structured triage suggestion from a natural language symptom description. It identifies matched red flags, rationale, recommended next steps, and safety disclaimers without providing diagnosis or treatment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can under-triage serious symptoms and should not be treated as a dependable medical triage system.

Mitigation: Use it only as a rough demonstration unless red-flag matching, low-confidence fallback behavior, and disclaimer display are reviewed and fixed for the intended workflow.

Risk: Case-insensitive matching and the claimed Chinese-language support may be incomplete, which can miss relevant red flags.

Mitigation: Validate multilingual and mixed-case symptom examples against expected triage outcomes before any real medical use.

Risk: Unnecessary requirements entries can create avoidable install confusion, and future unpinned dependencies could add supply-chain risk.

Mitigation: Remove unnecessary standard-library requirements and pin any future third-party dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/symptom-checker-triage)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown triage report or JSON object with CLI usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes triage level, confidence, red flags, rationale, recommendation, department, and medical disclaimer.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
