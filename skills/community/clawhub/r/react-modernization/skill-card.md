## Description:

React Modernization helps upgrade React applications by migrating class components to hooks, adopting React 18 and 19 features, running codemods, and adding TypeScript types.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to plan and execute React application migrations from class components to hooks, adopt React 18 and 19 APIs, run codemods, and add TypeScript typing while preserving behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends unpinned remote tools that can change after review and rewrite a project.

Mitigation: Pin installer and codemod versions or immutable commits, run migrations in a clean branch or sandbox, and inspect the full generated diff before committing changes.

Risk: React migration guidance can introduce behavior changes in state updates, effects, hydration, or concurrent rendering.

Mitigation: Apply migrations incrementally, keep comprehensive test coverage in place, and run the full test suite before merging changes.

## Reference(s):

- [React Modernization on ClawHub](https://clawhub.ai/wpank/skills/react-modernization)
- [artifact/SKILL.md](artifact/SKILL.md)
- [artifact/README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands]

**Output Format:** [Markdown guidance with TypeScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes migration checklists, codemod commands, search patterns, and React API examples.]

## Skill Version(s):

1.0.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
