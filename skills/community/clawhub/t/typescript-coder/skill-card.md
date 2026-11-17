## Description:

TypeScript Coder helps agents add or migrate TypeScript, configure type checking, fix TypeScript errors, add JSDoc annotations, and apply type-safe code patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhauga](https://clawhub.ai/user/jhauga)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to plan and implement TypeScript setup, JavaScript-to-TypeScript migration, type checking, tsconfig configuration, and type-safe code changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup or migration commands can change project dependencies, package scripts, configuration, or filenames.

Mitigation: Review proposed package.json, tsconfig, and file-renaming changes before applying them, and prefer pinned package versions and local project scripts.

Risk: Generated TypeScript guidance or code may introduce incorrect types, overly broad any usage, or misleading migration advice.

Mitigation: Run project type checks and review generated code for strictness, runtime behavior, and compatibility with existing build tooling.

## Reference(s):

- [TypeScript Coder Skill](artifact/SKILL.md)
- [TypeScript Basics](artifact/references/basics.md)
- [TypeScript Cheat Sheets](artifact/references/cheatsheet.md)
- [TypeScript Classes](artifact/references/classes.md)
- [TypeScript Elements](artifact/references/elements.md)
- [TypeScript Essentials](artifact/references/essentials.md)
- [TypeScript Keywords](artifact/references/keywords.md)
- [TypeScript Miscellaneous](artifact/references/miscellaneous.md)
- [TypeScript Types](artifact/references/types.md)
- [TypeScript Official Documentation](https://www.typescriptlang.org/docs/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
- [TypeScript tsconfig Reference](https://www.typescriptlang.org/tsconfig/)
- [TypeScript Deep Dive](https://basarat.gitbook.io/typescript/)
- [TypeScript Playground](https://www.typescriptlang.org/play)

## Skill Output:

**Output Type(s):** [Guidance, Code, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with TypeScript, JSON, JavaScript, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose package installation commands, tsconfig settings, file renames, type definitions, and code edits for review before application.]

## Skill Version(s):

3.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
