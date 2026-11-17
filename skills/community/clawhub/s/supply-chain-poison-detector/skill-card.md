## Description:

Helps detect supply chain poisoning in AI agent marketplace skills by scanning Gene/Capsule validation fields for shell injection, outbound requests, and encoded payloads that may indicate backdoors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud)

### License/Terms of Use:


## Use Case:

Developers and security reviewers use this skill to triage AI marketplace skills for possible supply chain poisoning before installation. It reviews pasted Capsule/Gene JSON, source code, or a provided asset URL and returns suspicious patterns, risk level, and recommended action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may review unsafe skill text or inspect a provided asset URL.

Mitigation: Provide only artifacts intended for review and avoid including private credentials or unrelated sensitive files.

Risk: The artifact contains dangerous command strings as scanner examples.

Mitigation: Treat those strings as examples for detection and do not execute example payloads.

Risk: Static pattern checks can miss sophisticated obfuscation, multi-stage payloads, or novel attack techniques.

Mitigation: Use the report as triage and manually review source code before installing skills with suspicious or unclear results.

## Reference(s):

- [Supply Chain Poison Detector on ClawHub](https://clawhub.ai/andyxinweiminicloud/skills/supply-chain-poison-detector)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown structured report with suspicious pattern findings, line references, risk rating, and recommended action]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Risk ratings use CLEAN, SUSPECT, and THREAT labels.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
