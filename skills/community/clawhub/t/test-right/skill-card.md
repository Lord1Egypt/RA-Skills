## Description:

Carry out useful testing of the user's target by choosing meaningful checks, preserving ordinary requests in comparisons, and inspecting the results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redrookai](https://clawhub.ai/user/redrookai)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and other users use TestRight to run focused tests of software, workflows, skills, and other targets, then assess the observed results. It helps keep comparisons fair and conclusions grounded in evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Testing, including delegated checks or model calls, can exceed the user's intended execution or spending scope.

Mitigation: Set clear test, execution, data, and spending limits before running checks.

Risk: The optional helper saves experiment input copies locally, which may contain sensitive test material.

Mitigation: Protect local input files and avoid placing sensitive material in experiments unless appropriate safeguards are in place.

Risk: Input consistency checks do not guarantee complete runtime isolation between comparison conditions.

Mitigation: Treat the helper as protection against accidental input changes, not as a security boundary; review the actual runner and inaccessible boundaries.

## Reference(s):

- [TestRight release on ClawHub](https://clawhub.ai/redrookai/skills/test-right)
- [Research Behind TestRight](REFERENCES.md)
- [AI Comparisons](references/ai-comparisons.md)
- [Optional Input Guard](references/input-guard.md)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Shell commands, JSON]

**Output Format:** [Markdown test findings with optional shell commands and JSON input packets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report the checks performed and their observed results; the optional input guard writes experiment input packets locally.]

## Skill Version(s):

0.1.2 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
