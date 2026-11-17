## Description:

Xiwang Medical Research helps agents search a local corpus of Xiwang Group graphene medical research documents by keyword, topic, or disease and draft evidence-grounded Chinese video scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ling61616161-dotcom](https://clawhub.ai/user/ling61616161-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to retrieve Xiwang graphene medical research from a local document corpus and turn selected results into Chinese health education, brand, or product-promotion video scripts for reviewer approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can recursively read documents from any caller-supplied directory.

Mitigation: Use it only with the intended medical research corpus and avoid pointing it at broad personal or business folders.

Risk: Generated scripts may include serious disease-treatment or product-promotion claims.

Mitigation: Have qualified medical and legal reviewers check generated content before publication.

Risk: The security evidence marks the release as suspicious because medical-claim generation has limited safety guardrails.

Mitigation: Review the skill before installing and require source-backed, non-absolute medical wording in outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ling61616161-dotcom/skills/xiwang-medical-research)
- [Document index](references/document_index.md)
- [Medical topics and disease mapping](references/medical_topics.md)
- [Video script guide](references/video_script_guide.md)
- [Video script template](assets/video_script_template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [JSON search results and Markdown video scripts with source notes and compliance reminders.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search commands require a caller-supplied local document directory; generated medical promotional content needs qualified review before publication.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
