## Description:

Builds, debugs, and reviews Svelte and SvelteKit apps, including runes, stores, snippets, load functions, form actions, and adapters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build, debug, migrate, test, and deploy Svelte and SvelteKit applications. It focuses on Svelte 5 runes, SvelteKit request handling, SSR and hydration issues, form actions, TypeScript, testing, performance, and deployment workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read and update Svelte-specific preference files under ~/Clawic/data/svelte/.

Mitigation: Review the disclosed preference path before installation and keep only non-sensitive project preferences in those files.

Risk: The skill includes npx examples that may resolve tools dynamically.

Mitigation: Review commands before execution and prefer project-local, lockfile-pinned tools or explicit package versions in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/svelte)
- [Clawic Svelte skill page](https://clawic.com/skills/svelte)
- [Svelte skill definition](artifact/SKILL.md)
- [Svelte setup and memory guidance](artifact/setup.md)
- [Svelte security guidance](artifact/security.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read or update user preference files under ~/Clawic/data/svelte/ when recording explicit user preferences.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
