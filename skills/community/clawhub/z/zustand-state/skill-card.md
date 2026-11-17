## Description:

Zustand state management for React and vanilla JavaScript. Use when creating stores, using selectors, persisting state to localStorage, integrating devtools, or managing global state without Redux complexity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill for guidance and code examples when adding Zustand stores, selectors, middleware, persistence, testing patterns, and TypeScript typing to React or vanilla JavaScript applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persisted Zustand state can expose secrets, auth tokens, or sensitive personal data if broad state snapshots are written to browser or device storage.

Mitigation: Persist only explicit non-sensitive keys with partialize or a reviewed full-state snapshot, and exclude secrets, auth tokens, and sensitive personal data.

Risk: DevTools middleware in shipped bundles can expose state or action details outside a development workflow.

Mitigation: Gate DevTools to development builds or document the production need during review before shipping.

## Reference(s):

- [Middleware](artifact/references/middleware.md)
- [Patterns & Best Practices](artifact/references/patterns.md)
- [TypeScript Patterns](artifact/references/typescript.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript and JavaScript code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only output; no hidden execution, data exfiltration, or agent persistence was reported by security evidence.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
