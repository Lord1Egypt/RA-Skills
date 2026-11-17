## Description:

Redux-Saga best practices, patterns, and API guidance for building, testing, and debugging generator-based side-effect middleware in Redux applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anivar](https://clawhub.ai/user/anivar)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering agents use this skill to write, review, test, and debug Redux-Saga workflows in JavaScript and TypeScript Redux applications, including concurrency, cancellation, channels, error handling, and Redux Toolkit integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The README recommends unpinned global installation commands that can fetch mutable remote code and persistently change agent behavior.

Mitigation: Install from a pinned package version or immutable commit when possible, and use global installation only when this skill should be available across agent contexts.

Risk: Example snippets for analytics, auth tokens, and storage may touch sensitive application data if copied without project-specific controls.

Mitigation: Adapt those snippets with normal privacy and security review for the target application before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anivar/skills/redux-saga-skill)
- [Metadata source URL](https://github.com/anivar/redux-saga-skill)
- [Publisher website](https://anivar.net)
- [Effects and API Reference](references/effects-and-api.md)
- [Fork Model and Concurrency](references/fork-model.md)
- [Testing Redux Sagas](references/testing.md)
- [Channels and External I/O](references/channels.md)
- [Recipes and Common Patterns](references/recipes.md)
- [Redux-Saga Anti-Patterns](references/anti-patterns.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and TypeScript code examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets redux-saga 1.4.2, Redux Toolkit integration, and redux-saga-test-plan testing patterns.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
