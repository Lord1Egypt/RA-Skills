## Description:

Scaffold and configure a production-ready SvelteKit PWA with opinionated defaults for TypeScript, Tailwind, component libraries, testing, linting, and deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leo3linbeck](https://clawhub.ai/user/leo3linbeck)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to plan, scaffold, configure, test, and deploy SvelteKit web applications and PWAs with user review checkpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run package managers and scaffolding tools that may fetch mutable third-party code.

Mitigation: Run scaffolding in an isolated workspace and pin or approve exact tool and package versions before execution.

Risk: The skill can create repositories, push generated code, and deploy applications with unclear production boundaries.

Mitigation: Review diffs before commits and pushes, protect the main branch, and require a separate approval gate before production deployment.

## Reference(s):

- [SvelteKit State Management](https://svelte.dev/docs/kit/state-management)
- [GitHub CLI](https://cli.github.com)
- [Vercel Dashboard](https://vercel.com/new)
- [CLI Commands Reference](references/cli-commands.md)
- [Deployment Configuration](references/deployment.md)
- [PWA Configuration](references/pwa-config.md)
- [Ralph Implementation Plan](references/ralph-plan-template.md)
- [Ralph Agent Prompt](references/ralph-prompt.md)
- [Scaffold & Configure Story Templates](references/scaffold-stories.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code snippets, shell commands, configuration files, PRD/user-story JSON, and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce project files, deployment guidance, admin documentation, and live URL handoff details when approved by the user.]

## Skill Version(s):

1.1.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
