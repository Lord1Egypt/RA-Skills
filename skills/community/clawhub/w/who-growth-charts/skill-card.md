## Description:

Generate WHO child growth charts for height, weight, and BMI with percentile curves and child measurement overlays using WHO reference data downloaded on demand.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odrobnik](https://clawhub.ai/user/odrobnik)

### License/Terms of Use:


## Use Case:

External users, caregivers, and developers use this skill to generate local WHO percentile charts for a child's height, weight, or BMI from supplied measurement data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Child measurement data and generated charts may contain sensitive health information.

Mitigation: Keep input JSON, generated charts, and cached files in a private directory with appropriate local access controls.

Risk: The documented /tmp/withings.json pattern may expose imported measurement data on shared systems.

Mitigation: Use a secure temporary file, a private workspace path, or a direct pipe instead of a predictable /tmp path.

Risk: Unpinned Python dependencies can change behavior across installations.

Mitigation: Install the skill in a virtual environment and prefer pinned versions of pandas, matplotlib, scipy, and openpyxl.

Risk: The skill downloads WHO reference files and caches them locally.

Mitigation: Run it where outbound access to the WHO CDN is expected and review cached files according to local data handling policy.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/odrobnik/skills/who-growth-charts)
- [WHO Child Growth Standards reference data](https://cdn.who.int/media/docs/default-source/child-growth/child-growth-standards/indicators)
- [WHO Growth Reference 5-19 years data](https://cdn.who.int/media/docs/default-source/child-growth/growth-reference-5-19-years)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance with shell commands; generated PNG chart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local chart images and caches downloaded WHO reference files under who-growth-charts/ by default.]

## Skill Version(s):

1.2.3 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
