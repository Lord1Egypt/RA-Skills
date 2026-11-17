## Description:

Decodes veterinary visit notes, discharge summaries, and lab panels into plain language, evaluates species- and breed-aware abnormalities, tracks concerning trends, and generates questions for a veterinary follow-up.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to translate veterinary notes and pet lab results into educational plain-language summaries, abnormal-finding tables, trend notes, CKD staging context, and questions to bring to a veterinarian.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The veterinary lab interpreter can misread units or invalid numeric values while claiming to check unit mismatches.

Mitigation: Review before installing for reliable lab interpretation, verify every unit and reference range against the actual lab report, and add unit parsing, finite-value checks, and plausible bounds checks.

Risk: Educational veterinary interpretation could be mistaken for diagnosis, treatment advice, emergency triage, or a substitute for the attending veterinarian.

Mitigation: Keep outputs educational, confirm CKD staging and abnormal results with a veterinarian, and do not use the skill for emergency triage, prescribing, dosage calculations, or contradicting the attending veterinarian.

Risk: The server security verdict is suspicious because of reliability concerns rather than malicious behavior.

Mitigation: Treat outputs as educational only and review the ClawHub security summary and guidance before deployment.

## Reference(s):

- [Veterinary Lab Reference Ranges](references/lab-ranges.md)
- [Veterinary Abbreviation Glossary](references/abbreviations.md)
- [ClawHub skill page](https://clawhub.ai/voronindenis5/skills/vet-translator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with plain-language summaries, abnormal-finding tables, trend notes, question lists, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes educational-only veterinary framing and reminders to confirm interpretations with a veterinarian.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
