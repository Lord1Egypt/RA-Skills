## Description:

Bootstrap a fresh VPS with WordPress installed and verified end-to-end; use when you need to provision the stack, align volumes and environment variables, run WP-CLI installation, and confirm the public site is live.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarezoe](https://clawhub.ai/user/clarezoe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to provision a Docker-based WordPress site on a fresh VPS, manage the stack through Dokploy, run WP-CLI installation against the live volume, and verify that the public site is reachable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to make privileged, persistent changes on a live VPS.

Mitigation: Require explicit confirmation of the target server, public domain, Dokploy project, and compose path before running deployment or compose commands.

Risk: WordPress and database credentials may be exposed through command lines, logs, or copied shell history.

Mitigation: Use a protected environment file or secret manager for credentials, avoid printing secrets, and do not pass long-lived passwords directly on command lines.

Risk: Unpinned WP-CLI and Docker image references can change behavior between runs.

Mitigation: Pin and verify WP-CLI and Docker image versions before deployment.

Risk: Using curl with disabled certificate verification can hide TLS or routing problems.

Mitigation: Use certificate-validating checks for final deployment verification and remove curl -k from completion criteria.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clarezoe/skills/wordpress-vps-install)
- [Publisher profile](https://clawhub.ai/user/clarezoe)
- [WP-CLI Phar download](https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Markdown]

**Output Format:** [Markdown with inline bash, Docker Compose, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-confirmed VPS, domain, WordPress admin, database, and deployment targets before execution.]

## Skill Version(s):

1.3.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
