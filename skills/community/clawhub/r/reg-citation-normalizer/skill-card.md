## Description:

Recognize, parse and normalize medical-device regulatory citations (21 CFR, ISO/IEC, Chinese GB/YY-T, NMPA decrees) into a canonical structure with recommended standard formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

Regulatory writers, translators, and medical-device documentation reviewers use this skill to identify and standardize citation formatting in registration dossiers, instructions for use, and technical files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document checks may echo short excerpts of user-provided text.

Mitigation: Limit access to check output and avoid sharing excerpts from sensitive documents.

Risk: Normalized citations do not establish that a regulation or clause is current or legally correct.

Mitigation: Verify citation details and current status against authoritative regulatory and standards sources before relying on them.

## Reference(s):

- [eCFR regulatory text](https://www.ecfr.gov/)
- [ISO standards](https://www.iso.org/)
- [China national standards information](https://openstd.samr.gov.cn/)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Plain text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can flag citation-formatting issues in documents; check mode returns a warning exit code when issues are found.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
