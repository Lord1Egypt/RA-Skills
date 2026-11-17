## Description:

Run a chained build, ship, verify, and notify pipeline for multi-segment feature work so each coding-agent task is committed, deployed, and verified before the next segment starts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fernando-fernandez3](https://clawhub.ai/user/fernando-fernandez3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Ship Loop to coordinate multi-feature implementation through agent coding, preflight checks, deployment verification, and repair loops. It is intended for trusted repositories where automated commits, pushes, and deployment checks are part of the normal release workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run configured agent, preflight, and deployment commands with the user's privileges.

Mitigation: Install only for trusted repositories and review SHIPLOOP.yml as executable code before running the pipeline.

Risk: Automation can change, commit, push, or discard repository work during repair and deployment flows.

Mitigation: Run from a clean branch after committing or stashing unrelated work, and review generated changes before accepting them.

Risk: Permission-bypass agent modes and meta or optimization loops can increase the blast radius on untrusted projects.

Mitigation: Avoid permission-bypass agent modes unless necessary, and disable meta or optimization learnings for untrusted projects.

Risk: The bundled documentation dependencies may be stale.

Mitigation: Update documentation dependencies before building or publishing the docs site.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fernando-fernandez3/skills/ship-loop)
- [PyPI Project](https://pypi.org/project/shiploop/)
- [Skill README](README.md)
- [Configuration Reference](docs/src/content/docs/reference/configuration.md)
- [CLI Reference](docs/src/content/docs/reference/cli.md)
- [Architecture](docs/src/content/docs/concepts/architecture.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and terminal-oriented status output with configuration examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create commits, update project files, run configured preflight commands, push to a remote, and record run history when executed in a repository.]

## Skill Version(s):

5.0.0 (source: server release metadata, openclaw metadata, pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
