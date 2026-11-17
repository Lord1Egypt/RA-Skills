## Description:

Zod v4 best practices, patterns, and API guidance for schema validation, parsing, error handling, and type inference in TypeScript applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anivar](https://clawhub.ai/user/anivar)

### License/Terms of Use:

MIT

## Use Case:

Developers and software engineering agents use this skill to write, review, and debug Zod v4 schemas in TypeScript projects. It focuses on runtime validation at system boundaries, type inference, object composition, refinements, transforms, error handling, observability, and v3-to-v4 migration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing globally or from an unpinned source can make the skill available across projects and may pick up unexpected changes.

Mitigation: Prefer a pinned skill source or reviewed commit, and use global installation only when cross-project availability is intended.

Risk: Copying CI `npx` examples directly can introduce normal JavaScript supply-chain drift.

Mitigation: Adapt CI examples to pinned dev dependencies or locked package scripts before production use.

Risk: The guidance targets Zod v4 and TypeScript ^5.5; applying it to other major versions may produce incompatible recommendations.

Mitigation: Confirm project dependency versions before applying migration or API guidance.

## Reference(s):

- [Schema Types](references/schema-types.md)
- [Parsing and Inference](references/parsing-and-inference.md)
- [Objects and Composition](references/objects-and-composition.md)
- [Refinements and Transforms](references/refinements-and-transforms.md)
- [Error Handling](references/error-handling.md)
- [Advanced Features](references/advanced-features.md)
- [Anti-Patterns](references/anti-patterns.md)
- [Boundary Architecture](references/boundary-architecture.md)
- [Linter and CI](references/linter-and-ci.md)
- [Skill Metadata Source URL](https://github.com/anivar/zod-skill)
- [Skill Metadata Author URL](https://anivar.net)
- [ClawHub Skill Page](https://clawhub.ai/anivar/skills/zod-skill)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with TypeScript and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable payload; guidance is scoped to TypeScript ^5.5 projects using zod ^4.0.0.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
