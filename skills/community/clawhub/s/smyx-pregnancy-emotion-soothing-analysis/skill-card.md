## Description:

The skill submits supplied video, with optional audio, for analysis of behaviors described as emotional distress during pregnancy and returns the resulting report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

A user can submit a pregnancy-related recording for behavioral analysis, review the resulting report and suggestions, or query prior reports. The documentation describes this as emotional support rather than medical diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the release suspicious, citing a mismatch between the advertised pregnancy emotion monitoring and reported on-demand video analysis, as well as privacy-sensitive uploads and account setup that may occur without clear disclosure.

Mitigation: Before installation or use, confirm the actual behavior and verify who receives video and identity details, what is retained, and whether uploads and account enrollment can be explicitly authorized or avoided.

Risk: The security scan was partial because a referenced local path was missing, so the available evidence does not establish what that reference contains.

Mitigation: Review the missing reference and obtain a complete scan before relying on the release.

## Reference(s):

- [API interface documentation](references/api_doc.md)
- [Skill demo](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Files]

**Output Format:** [Structured analysis report as JSON or text; history results may be shown as a Markdown table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include behavioral observations, suggestions, and report links; results can optionally be saved to a local file]

## Skill Version(s):

1.0.18 (source: server-resolved release metadata; bundled frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
