## Description:

Use when executing implementation plans with independent tasks in the current session. Features domain-specialist routing, independent verification gates, and systematic failure recovery for high-quality parallel-safe execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forestwolf713](https://clawhub.ai/user/forestwolf713)

### License/Terms of Use:


## Use Case:

Developers and engineering agents use this skill to execute mostly independent implementation-plan tasks in the current session with subagent implementation, independent test verification, specialist spec review, and code quality review gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow delegates planned coding work to subagents that may edit code, run tests, and create commits.

Mitigation: Review the plan before invoking the skill and keep review gates active until verification, spec compliance, and code quality issues are resolved.

Risk: Multiple implementation subagents can conflict if they work in parallel on the same codebase.

Mitigation: Dispatch one implementation subagent per task in sequence and provide each subagent with the extracted task text and relevant context.

## Reference(s):

- [Subagent Driven Development on ClawHub](https://clawhub.ai/forestwolf713/skills/subagent-driven-development-3)
- [forestwolf713 publisher profile](https://clawhub.ai/user/forestwolf713)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown instructions with prompt templates, workflow steps, review gates, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Coordinates subagent task execution and review loops; does not produce standalone executable software.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
