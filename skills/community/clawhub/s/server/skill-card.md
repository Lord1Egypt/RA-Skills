## Description:

Helps agents operate web and application services on a host, including supervision, proxy routing, worker sizing, deployment, rollback, logs, TLS reloads, static assets, and self-hosted applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to diagnose, configure, deploy, and maintain services running on hosts, especially when proxying, process supervision, capacity, logs, TLS reloads, or rollback behavior matters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A hardening sweep command may start at the filesystem root and scan the whole host for credential-like files.

Mitigation: Before use, limit that sweep to known document roots or service directories and avoid running it broadly on shared or privileged hosts.

Risk: The skill maintains local operational notes and may update or delete rows it wrote as part of normal maintenance.

Mitigation: Review the configured Clawic data paths and keep operational notes under the documented local directories; do not store secret values there.

## Reference(s):

- [Server skill on ClawHub](https://clawhub.ai/ivangdavila/skills/server)
- [Server skill homepage](https://clawic.com/skills/server)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands, code snippets, configuration examples, and operational guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and update local operational notes under configured Clawic data paths; secret values are represented as pointers rather than stored directly.]

## Skill Version(s):

1.0.2 (source: server evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
