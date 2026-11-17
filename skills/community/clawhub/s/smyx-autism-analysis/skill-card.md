## Description:

Performs special video analysis on behavioral characteristics of children with autism, identifies core symptom features, provides structured analysis reports and intervention recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

External users and care-related professionals use this skill to submit child behavior videos or URLs for ASD-oriented screening support, structured analysis reports, and intervention suggestions. The output is screening guidance only and does not replace professional medical diagnosis or clinical evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags this skill as suspicious because it handles children's health videos with under-disclosed cloud upload, automatic identity/account handling, local token storage, and insecure HTTP endpoints.

Mitigation: Review carefully before installing; do not use real child videos or identifiable health-related media unless the publisher documents recipients, retention and deletion terms, HTTPS-only transport, token protection, and explicit consent or authorization.

Risk: The skill produces ASD screening-oriented analysis that may be mistaken for clinical diagnosis.

Mitigation: Use outputs as early screening support only and refer suspected ASD cases to qualified medical or clinical professionals for evaluation.

## Reference(s):

- [API Interface Documentation](references/api_doc.md)
- [Skill Demo](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summaries or JSON-formatted structured analysis results, depending on detail level.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return ASD behavior analysis findings, risk or screening indicators, intervention suggestions, historical report lists, and report links.]

## Skill Version(s):

1.0.13 (source: server release evidence; artifact frontmatter reports 1.0.14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
