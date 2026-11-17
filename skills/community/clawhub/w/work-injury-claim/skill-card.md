## Description:

Work Injury Claim helps injured workers in China assess work-injury recognition, prepare claim materials, estimate benefits, check regional rules, and generate claim documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyue71](https://clawhub.ai/user/wangyue71)

### License/Terms of Use:

MIT-0

## Use Case:

External users in China use this skill for work-injury recognition, labor-capacity assessment preparation, benefit estimation, claim material checklists, and claim document drafting. The skill is a reference aid and does not replace current local policy checks or professional legal advice.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill can handle sensitive legal, medical, identity, employment, and payment details.

Mitigation: Use redacted drafts where possible, avoid full ID numbers, bank details, complete medical records, or private documents unless necessary, and generate files only in a private folder.

Risk: Claim guidance, legal citations, regional rules, disability references, and compensation estimates may be incomplete or outdated.

Mitigation: Treat outputs as reference material, verify current local rules with 12333 or a qualified lawyer, and do not rely on compensation amounts or legal citations as final advice.

Risk: Generated claim documents may include sensitive user-provided facts and may be unsuitable for direct submission.

Mitigation: Review generated documents before sharing or filing, remove unnecessary private details, and consult appropriate professionals for complex or high-value claims.

## Reference(s):

- [Work Injury Recognition Reference](references/work_injury_recognition.md)
- [Claim Documents Checklist](references/claim_documents.md)
- [Labor Capacity Assessment Reference](references/disability_assessment.md)
- [Compensation Calculation Reference](references/compensation_calculation.md)
- [Regional Rules Reference](references/regional_differences.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with optional generated Markdown claim documents and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate a work-injury recognition application, compensation table, and claim materials checklist as Markdown files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
