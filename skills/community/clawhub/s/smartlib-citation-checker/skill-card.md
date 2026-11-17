## Description:

Checks references in papers or AI-generated bibliographies against SmartLib records, identifies mismatches, and produces an HTML verification report with corrected citations and source links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j-levee](https://clawhub.ai/user/j-levee)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and academic writers can check whether citations in a paper draft or AI-generated reference list match SmartLib records, review suggested corrections, and export a verification report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment marks the release suspicious and reports an exposed production gateway credential.

Mitigation: Avoid relying on credentials bundled with the package; have the credential owner revoke or rotate the exposed credential, and review credential handling before use.

Risk: The security assessment reports risky account and notification instructions, and says inspection was incomplete (4 of 6 components scanned, with one referenced sample only partly inspected).

Mitigation: Review the account and notification steps and inspect the remaining content before enabling the skill; use extra caution in shared environments.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/j-levee/skills/smartlib-citation-checker)
- [Publisher profile](https://clawhub.ai/user/j-levee)

## Skill Output:

**Output Type(s):** [HTML report, Text, Guidance]

**Output Format:** [HTML verification report with result tables, corrected references, source links, and citation statistics; corrected references can also be downloaded as plain text.]

**Output Parameters:** [1D (one paper draft or reference list)]

**Other Properties Related to Output:** [Supports GB/T 7714, APA, MLA, Chicago, and BibTeX formats; reports citation matches and field-level differences.]

## Skill Version(s):

3.6.8 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
