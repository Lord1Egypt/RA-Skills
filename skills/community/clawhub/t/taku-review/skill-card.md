## Description:

Taku Review reviews implementation diffs after build work, checking for security issues, bugs, code quality concerns, scope drift, and verification evidence before shipping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kkenny0](https://clawhub.ai/user/kkenny0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Taku Review after implementation to inspect repository diffs, identify blocking delivery risks, and summarize verification evidence and residual concerns before merging or shipping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically edit repository files during review when it considers a fix clear.

Mitigation: Review local diffs after each run and invoke it only when code review plus possible fixes are intended.

## Reference(s):

- [Taku Review ClawHub skill page](https://clawhub.ai/kkenny0/skills/taku-review)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Structured Markdown with HARD STOPS, CONCERNS, and SUMMARY sections; may include code edits or shell commands when auto-fixing clear issues.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires visible verification evidence before reporting a change as ready to ship.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
