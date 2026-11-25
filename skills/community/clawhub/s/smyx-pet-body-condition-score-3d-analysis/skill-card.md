## Description:

Analyzes multi-angle pet videos to estimate body shape and a 1–9 Body Condition Score (BCS), returning structured weight-management observations without diagnosing disease or recommending treatment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Pet-care teams and developers can use this skill to estimate a cat’s or dog’s body condition from multi-angle video and review structured observations for weight management. Results are visual estimates and are not veterinary diagnoses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence flags identity and credential handling, account creation, and access to report history; scanner coverage is partial.

Mitigation: Review identity, credential, and report-data handling before installation, and grant access only to trusted users and services.

Risk: Security evidence reports that an export-only option may still run analysis.

Mitigation: Treat export-only mode as potentially executing analysis until verified, and avoid using sensitive video inputs with it.

## Reference(s):

- [Pet health analysis API documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-pet-body-condition-score-3d-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured BCS report in JSON or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a BCS score, body-condition category, observations, and report links; visual estimates may differ from palpation.]

## Skill Version(s):

1.0.16 (source: server-resolved release metadata; artifact frontmatter reports 1.0.23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
