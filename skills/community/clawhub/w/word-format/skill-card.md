## Description:

Converts uploaded Word documents into a fixed Chinese official-document format using the bundled template rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nighmat1220](https://clawhub.ai/user/nighmat1220)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and document-preparation agents use this skill to restyle `.docx` files into a prescribed Chinese official-document format and return a converted document when required fonts are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Oversized or crafted DOCX files may consume excessive CPU or memory during conversion.

Mitigation: Use trusted documents when possible and run conversion in a resource-limited environment for untrusted inputs.

Risk: The converted document may not preserve complex layouts perfectly.

Mitigation: Manually review complex documents after conversion before relying on the output.

Risk: Conversion stops when required fonts are unavailable.

Mitigation: Install the required fonts before use and treat missing-font output as a hard failure rather than a completed conversion.

## Reference(s):

- [Format Rules](artifact/references/format-rules.md)
- [ClawHub Skill Page](https://clawhub.ai/nighmat1220/skills/word-format)
- [Publisher Profile](https://clawhub.ai/user/nighmat1220)

## Skill Output:

**Output Type(s):** [Files, Text, Shell commands, Guidance]

**Output Format:** [Converted DOCX file with plain-text status or missing-font messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a DOCX input file and the listed fonts; complex layouts should be manually reviewed after conversion.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
