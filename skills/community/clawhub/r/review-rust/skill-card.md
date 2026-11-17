## Description:

Comprehensive Rust code review that fans out across detected technology areas, running them in parallel when the agent supports subagents and sequentially otherwise.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering reviewers use this skill for pre-push or pre-PR Rust code review of .rs files, including checks for language, async, database, serialization, testing, unsafe, FFI, concurrency, macro, and public API concerns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cargo checks, Clippy, and tests may execute code from the reviewed repository.

Mitigation: Use the skill only on Rust projects you are comfortable allowing an agent to inspect and build, and treat third-party or untrusted repositories as higher risk.

Risk: The review flow can load sibling review skills for specialized Rust technology areas.

Mitigation: Verify that any sibling review skills loaded during use are trusted before relying on their guidance.

## Reference(s):

- [Review Rust on ClawHub](https://clawhub.ai/anderskev/skills/review-rust)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown review report with command snippets and severity-ranked findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a review summary, issues grouped by severity, good patterns, and a verdict.]

## Skill Version(s):

1.0.4 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
