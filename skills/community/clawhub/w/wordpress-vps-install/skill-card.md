## Description: <br>
Bootstrap a fresh VPS with WordPress installed and verified end-to-end; use when you need to provision the stack, align volumes and environment variables, run WP-CLI installation, and confirm the public site is live. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clarezoe](https://clawhub.ai/user/clarezoe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to bootstrap a Docker-based WordPress installation on a fresh VPS, manage the deployment through Dokploy, run WordPress setup against the live volume, and verify the public site. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides system-changing WordPress deployment actions that can affect a VPS, domain routing, containers, volumes, and credentials. <br>
Mitigation: Use it only on a fresh or explicitly approved VPS and domain, and confirm the host, Dokploy project, domain, credentials, and backups before running deployment commands. <br>
Risk: The workflow includes a WP-CLI download step for operational tooling. <br>
Mitigation: Consider replacing that step with a pinned, checksum-verified WP-CLI release before use in stricter environments. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell, Docker Compose, and WP-CLI command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.3.2 (source: evidence.release.version and artifact frontmatter metadata.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
