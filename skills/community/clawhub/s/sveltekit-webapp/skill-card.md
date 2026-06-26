## Description: <br>
Scaffold and configure a production-ready SvelteKit PWA with opinionated defaults for TypeScript, Tailwind, UI components, testing, linting, and deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leo3linbeck](https://clawhub.ai/user/leo3linbeck) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to plan, scaffold, test, and deploy SvelteKit PWAs through a guided PRD, preflight, implementation, staging, and production workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can scaffold, modify, test, commit, and potentially deploy a SvelteKit application using shell commands and external CLIs. <br>
Mitigation: Approve use only for the intended target directory and repository, and review proposed shell commands before execution. <br>
Risk: Staging or production workflows can depend on active GitHub, Vercel, Turso, OAuth, database, or payment credentials. <br>
Mitigation: Confirm account identity, repository privacy, branch names, environment variables, and deployment intent before approving staging or production actions. <br>
Risk: Generated PRD, application code, or deployment configuration may not match product, privacy, or security expectations. <br>
Mitigation: Use the documented PRD approval, index-page checkpoint, preflight, typecheck, unit test, and E2E test gates before deployment. <br>


## Reference(s): <br>
- [Skill source](SKILL.md) <br>
- [CLI Commands Reference](references/cli-commands.md) <br>
- [Deployment Configuration](references/deployment.md) <br>
- [PWA Configuration](references/pwa-config.md) <br>
- [Ralph Implementation Plan](references/ralph-plan-template.md) <br>
- [Scaffold & Configure Story Templates](references/scaffold-stories.md) <br>
- [SvelteKit state management documentation](https://svelte.dev/docs/kit/state-management) <br>
- [GitHub CLI](https://cli.github.com) <br>
- [Vercel project creation](https://vercel.com/new) <br>
- [Skeleton documentation](https://skeleton.dev/docs/get-started) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON snippets, code blocks, and shell command sequences] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create project files, PRD JSON, tests, commits, repository setup, and deployment instructions after user approval.] <br>

## Skill Version(s): <br>
1.1.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
