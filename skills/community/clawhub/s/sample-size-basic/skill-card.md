## Description:

Basic sample size calculator for clinical research planning with common statistical scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Clinical researchers, study planners, and educators use this skill to estimate sample sizes for early clinical study planning across common statistical scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invalid or out-of-range statistical inputs may crash the tool or produce unreliable calculations.

Mitigation: Validate inputs before execution and review outputs as preliminary planning estimates rather than final clinical study determinations.

Risk: Scientific dependency versions can affect production reliability.

Mitigation: Install in an isolated Python environment and review or pin numpy and scipy before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/sample-size-basic)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text CLI output with numeric sample size estimates and statistical assumptions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires numeric inputs for test choice, alpha, power, and scenario-specific effect parameters.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
