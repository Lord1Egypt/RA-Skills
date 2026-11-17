## Description:

Router and map for the podcast/review-scout/ideation/signal-report skill family — explains what each skill does, when to reach for which one, and how the shared infra (render_report.py, template.html, analytics-check.md, per-skill ledgers) fits together. User-invoked only; never fires automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[orensegal](https://clawhub.ai/user/orensegal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this user-invoked routing guide to choose among the podcast, review-scout, and ideation skills or to find the shared signal-report renderer. It summarizes how the skills relate and where shared reporting and analytics components live.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review could not resolve some referenced local paths because those files were not included in the scanned artifact.

Mitigation: Check that the referenced files are present in the full release before relying on workflows that depend on them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/orensegal/skills/signal-skills-research-suite)
- [Signal Skills project homepage](https://github.com/OrenSegal/signal-skills)
- [Separate Signal Scout product mentioned in the skill](https://github.com/OrenSegal/signal-scout)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown routing and reference guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Explains skill selection and shared components; does not perform research itself.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
