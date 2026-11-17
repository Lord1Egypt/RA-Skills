## Description:

Use when asked to simplify, clean up, tidy, or refactor code for clarity without changing what it does, or when the user says "simplify this", "clean this up", "make it readable", "reduce the complexity", or "tidy this". Behavior-preserving only; not a bug or security audit (use bug-hunt or security-sweep for those).

This skill is ready for commercial/non-commercial use.

## Publisher:

[escoffier-labs](https://clawhub.ai/user/escoffier-labs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to make scoped, behavior-preserving code cleanup and document the changes with verification evidence. If behavior cannot be locked with tests, it switches to a report-only plan instead of applying edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A cleanup change could unintentionally alter behavior if the relevant behavior is not covered by verification.

Mitigation: Establish a baseline, make small scoped changes, and rerun the same tests; switch to report mode when behavior cannot be locked.

Risk: Running project tests executes local project code and may have side effects.

Mitigation: Review the test commands and run them only in an appropriate project environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/escoffier-labs/skills/skillet-reduce)

## Skill Output:

**Output Type(s):** [Code, Markdown, Shell commands, Guidance]

**Output Format:** [Behavior-preserving code edits or a Markdown simplification plan with verification evidence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scoped to requested or recently changed code; apply mode requires behavior-verification evidence]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
