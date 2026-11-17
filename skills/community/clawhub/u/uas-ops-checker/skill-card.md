## Description:

Classifies drones by weight for China-focused operational compliance decision support and returns structured JSON with obligations and review notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Drone operators and developers use this skill to estimate a Chinese drone weight class and associated obligations from maximum takeoff weight or empty weight. Results are decision support, not a compliance certificate or legal advice.

### Deployment Geography for Use:

China (regulatory scope)

## Known Risks and Mitigations:

Risk: Regulatory classifications, thresholds, or cited clauses may be inaccurate or outdated.

Mitigation: Treat results as non-authoritative decision support and check clauses and thresholds against current official sources before acting.

Risk: The skill lists Write and WebFetch permissions beyond its documented local CLI workflow.

Mitigation: Limit tool permissions to those needed for the intended workflow.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zhaoxinghua09-cell/skills/uas-ops-checker)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes classification, possible grades, obligations, warnings, clause review checklist, and status code.]

## Skill Version(s):

1.0.1 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
