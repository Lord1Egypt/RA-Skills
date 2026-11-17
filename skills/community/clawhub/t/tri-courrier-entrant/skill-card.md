## Description:

Trie un mail entrant pour détecter s'il concerne la comptabilité, extrait les pièces jointes et en-têtes utiles, sans analyser ou classer le contenu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trendex](https://clawhub.ai/user/trendex)

### License/Terms of Use:

MIT-0

## Use Case:

Accounting teams and workflow agents use this skill as the first step in an incoming-mail pipeline: it decides whether an email is accounting-related and extracts the email header fields and candidate attachments for downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email metadata and attachment paths may expose private mail or document locations outside the intended accounting workflow.

Mitigation: Use the skill only for the intended accounting email workflow and keep downstream processing scoped to accounting documents.

Risk: Keyword and attachment-extension triage can retain mail that is not accounting-related or flag messages whose body still needs review.

Mitigation: Route retained messages and extracted pieces through the downstream accounting-analysis steps or human review before classification or filing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/trendex/skills/tri-courrier-entrant)

## Skill Output:

**Output Type(s):** [JSON, Text guidance]

**Output Format:** [JSON object plus concise human-facing status sentence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not read attachment contents, classify documents, or write files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
