## Description:

Guides agents that build, debug, review, and test React applications, including components, hooks, state management, Server Components, forms, performance, and TypeScript patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to produce React components, state-management guidance, debugging steps, tests, TypeScript typings, setup commands, and code review findings for web applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional setup commands can affect the user's local project environment.

Mitigation: Run setup in a normal least-privileged project environment and consider pinning package versions before installing dependencies.

Risk: The skill uses a local memory file for project and preference notes.

Mitigation: Do not store secrets or sensitive credentials in ~/Clawic/data/react/memory.md.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/react)
- [Clawic React skill page](https://clawic.com/skills/react)
- [React Docs](https://react.dev)
- [Next.js Docs](https://nextjs.org/docs)
- [TanStack Query](https://tanstack.com/query)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code blocks and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local preference memory under ~/Clawic/data/react/ when present.]

## Skill Version(s):

1.0.7 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
