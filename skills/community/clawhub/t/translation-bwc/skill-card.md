## Description:

This skill helps agents translate BWC product, technical, and API documentation between Chinese and English while preserving approved terminology, code, identifiers, placeholders, and document structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyknowgen](https://clawhub.ai/user/cyknowgen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and localization reviewers use this skill to translate BWC product and API documentation between Chinese and English with locked glossary terms and preserved technical identifiers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generic translation triggers could cause the skill to be applied to content that is not actually about BWC.

Mitigation: Confirm the request is BWC-related before applying the glossary and style rules; use a generic translation workflow for unrelated content.

Risk: Incomplete glossary entries can lead to uncertain or inconsistent translations.

Mitigation: Flag missing terminology with [NEEDS-GLOSSARY] and ask for the approved BWC term list before production translation.

## Reference(s):

- [BWC Glossary - Terminology Source of Truth](references/glossary.md)
- [BWC Technical Translation Style Guide](references/style-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text translation output with preserved inline code, identifiers, placeholders, and review flags for missing glossary terms]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include inline [NEEDS-GLOSSARY] flags for BWC terms that are absent from the glossary.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
