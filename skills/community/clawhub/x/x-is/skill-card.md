## Description:

Value validation and environment detection tool for Shell scripts that validates input types, compares file ages, detects runtime environments, and supports batch checking through shell exit codes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lunrenyi](https://clawhub.ai/user/lunrenyi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to have an agent recall and propose `x is` shell validation commands for input checks, file freshness checks, variable-state checks, environment detection, and scripting pre-flight logic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested shell commands may be copied into scripts without checking whether the arguments, globs, or environment assumptions match the user's system.

Mitigation: Review each proposed command before execution, with particular attention to file-age checks that use globs and environment checks that control script branching.

Risk: The skill describes a silent validator whose success or failure is communicated through exit codes, so misuse can make script branches behave incorrectly.

Mitigation: Confirm the intended `x is` predicate and test representative passing and failing inputs before relying on the command in automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lunrenyi/skills/x-is)
- [Skill repository](https://github.com/x-cmd/skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill provides reference guidance and command examples; it does not execute commands by itself.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
