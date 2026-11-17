## Description:

Provides Python-focused guidance for writing, debugging, reviewing, packaging, typing, testing, performance tuning, concurrency, security, and version-upgrade work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when building or maintaining Python projects, especially when they need targeted guidance for debugging tracebacks, dependency and environment issues, typing, tests, CLI behavior, subprocesses, HTTP, files, SQLite, security, performance, or Python version upgrades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can cause an agent to suggest commands, dependency installs, and file edits that may affect local projects.

Mitigation: Review generated commands and diffs before applying them, and prefer explicit timeouts, tests, and reversible changes.

Risk: Per-user preferences can influence future Python guidance.

Mitigation: Review or clear ~/Clawic/data/py/config.yaml before using the skill in sensitive or tightly controlled contexts.

Risk: Python guidance may touch risky areas such as subprocesses, deserialization, SQL, paths, archives, TLS, and secrets.

Mitigation: Follow the skill's security guidance: avoid untrusted eval or pickle, parameterize SQL, avoid shell interpolation, contain filesystem paths, and keep secrets out of logs.

## Reference(s):

- [ClawHub Python skill listing](https://clawhub.ai/ivangdavila/skills/py)
- [Clawic Python skill homepage](https://clawic.com/skills/py)
- [Python skill source](artifact/SKILL.md)
- [Python security guide](artifact/security.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline code blocks, command examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use per-user preferences from ~/Clawic/data/py/config.yaml when present.]

## Skill Version(s):

1.0.4 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
