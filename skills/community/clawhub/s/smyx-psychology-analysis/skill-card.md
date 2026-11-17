## Description:

Provides an interface for submitting video for psychological analysis and returning structured reports and improvement suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals or organizations can submit local videos or video URLs for psychological analysis and retrieve previously generated reports. The documentation says reports are for reference and do not replace professional diagnosis or treatment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video uploads and remote account setup may involve sensitive data and stored credentials.

Mitigation: Before uploading, verify what video and identity data the service receives, what credentials it stores, and whether analysis can be avoided in export-only use; obtain consent and use only appropriate footage.

Risk: The advertised analysis capability may not match the supplied implementation, and scan coverage leaves some uncertainty.

Mitigation: Verify the available behavior and service responses before relying on reports; treat results as informational and seek qualified professional help for mental health concerns.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-psychology-analysis)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [API documentation](references/api_doc.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Report links]

**Output Format:** [Structured text or JSON reports, with report export links; results can be saved to a file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include suggested improvements; the documentation describes them as informational, not a professional diagnosis or treatment.]

## Skill Version(s):

1.0.26 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
