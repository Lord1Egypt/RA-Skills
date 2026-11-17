## Description:

Analyzes explicitly supplied relationship chat histories by cleaning noisy exports, segmenting episodes, and producing evidence-grounded findings about communication patterns, conflict cycles, repair attempts, boundaries, safety concerns, effort balance, and blind spots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yujun-bo2](https://clawhub.ai/user/yujun-bo2)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to analyze explicitly supplied romantic or relationship chat logs, especially long or noisy exports, for recurring communication patterns, conflict and repair cycles, effort balance, boundaries, and safety concerns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes intimate relationship chat records that may contain identifiers, sexual content, abuse disclosures, or third-party details.

Mitigation: Analyze only records the user explicitly provides or identifies, redact unnecessary identifiers, and avoid storing raw full chat logs.

Risk: Generated reports and manifests may persist in local backups, sync services, search indexes, or later processes.

Mitigation: Disclose planned output paths and write files only with user consent unless file output was explicitly requested.

Risk: Relationship analysis can overstate motives, diagnoses, or safety conclusions from incomplete chat evidence.

Mitigation: Separate observations from interpretations and uncertainty, avoid diagnosis or mind-reading, and flag safety concerns only from observable evidence.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yujun-bo2/skills/relationship-chat-analysis-skill)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [Detailed Implementation Guide](artifact/references/instructions.md)
- [Chat Cleaning And Normalization Prompt](artifact/references/cleaning-prompt.md)
- [Episode-Level Relationship Extraction Prompt](artifact/references/extraction-prompt.md)
- [Cross-Episode Relationship Synthesis Prompt](artifact/references/synthesis-prompt.md)
- [Relationship Blind Spot And Safety Review Prompt](artifact/references/blindspot-prompt.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown analysis report with optional redacted JSON corpus manifest]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses short supporting excerpts and avoids storing raw full chat logs by default.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
