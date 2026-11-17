## Description:

Use for Hong Kong school admissions, school selection, secondary school, primary school, kindergarten, international school, and postsecondary advisory workflows with SchoolFit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djanngau](https://clawhub.ai/user/djanngau)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to support Hong Kong school search, comparison, shortlisting, admissions, vacancy checks, application planning, and education-path advisory workflows. It turns family preferences into concise, evidence-grounded next steps while keeping official facts, non-official Band references, time-limited signals, and assumptions separate.

### Deployment Geography for Use:

Hong Kong

## Known Risks and Mitigations:

Risk: School-search preferences and the SchoolFit session access code are sent to schoolfit.hk for live queries.

Mitigation: Warn users before live queries, ask them to remove identifying family details, and keep the access code only in the active trusted one-to-one chat or current helper invocation.

Risk: The automatic privacy filter is incomplete and may not catch every identifying detail.

Mitigation: Require users to omit student names, home addresses, report-card text, private documents, HKID numbers, phone numbers, and other identifying family details before using live API commands.

Risk: Vacancy and admissions data are time-limited leads and may be stale or incomplete.

Mitigation: Present vacancy and admissions information as leads, not guarantees, and direct families to verify the latest status with the school.

## Reference(s):

- [ClawHub SchoolFit Skill Page](https://clawhub.ai/djanngau/skills/schoolfit)
- [Source Homepage](https://github.com/djanngau/schoolfit-skill)
- [SchoolFit](https://schoolfit.hk/)
- [SchoolFit Access Code](https://schoolfit.hk/skill-code)
- [SchoolFit Applications](https://schoolfit.hk/applications)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or JSON returned by helper commands, summarized as concise parent-facing guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live SchoolFit API queries require a SchoolFit access code; local parent-request parsing can run without contacting SchoolFit.]

## Skill Version(s):

1.3.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
