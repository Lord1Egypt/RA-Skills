## Description:

Design, review, or implement source-to-source code translation pipelines that convert or port code between programming languages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[syuaibsyuaib](https://clawhub.ai/user/syuaibsyuaib)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design, review, or implement bounded source-to-source code conversion pipelines with parser probes, semantic IR boundaries, lowering rules, diagnostics, and regression-oriented validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Implementation use may modify project source or test files while building a converter slice.

Mitigation: Review proposed edits, keep changes scoped to representative fixtures and tests, and run validation before adopting generated code.

Risk: Cross-language conversion can introduce semantic drift or silently mishandle unsupported constructs.

Mitigation: Use a supported-feature matrix, explicit diagnostics, parser probes, compile or type checks, and fixture-based tests before treating output as behavior-preserving.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/syuaibsyuaib/skills/universal-code-converter)
- [Architecture Blueprint](references/architecture-blueprint.md)
- [Validation Checklist](references/validation-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks, file edits, and shell commands when implementation is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include supported-feature matrices, known gaps, assumptions, warnings, validation plans, tests, and scoped converter implementation slices.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
