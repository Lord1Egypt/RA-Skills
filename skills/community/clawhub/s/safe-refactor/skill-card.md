## Description:

Safe Refactor guides an agent through behavior-preserving code refactors by requiring an explicit behavior contract, test coverage, a green baseline, small mechanical changes, verification after each step, and review of any behavior drift.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dennisrongo](https://clawhub.ai/user/dennisrongo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill when they need to restructure, rename, extract, inline, or split code while preserving existing observable behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A vague request such as "clean this up" may route the agent into a refactoring workflow when the user intended a bug fix or feature change.

Mitigation: Use explicit wording when requesting behavior changes, and split behavior-preserving refactors from bug fixes or feature work.

Risk: A refactor can silently change behavior if baseline tests are missing, failing, or not run.

Mitigation: Require a written behavior contract, covering tests or characterization tests for touched paths, a green baseline, and verification after each mechanical step.

Risk: Renames and moves can miss dynamic, serialized, or string-based references that the compiler does not check.

Mitigation: Grep for old names across code, strings, configuration, documentation, and serialized identifiers, then justify any remaining hits.

## Reference(s):

- [ClawHub safe-refactor skill page](https://clawhub.ai/dennisrongo/skills/safe-refactor)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands]

**Output Format:** [Markdown guidance with code references and shell command summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces refactor plans, behavior contracts, verification reports, grep results, and risk notes; it does not include hidden code or credential access.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
