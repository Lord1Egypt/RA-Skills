## Description:

Auto-discover and catalog all services in a codebase or organization by scanning Dockerfiles, docker-compose, Kubernetes manifests, package.json, systemd units, and Procfiles to generate a living service inventory with ownership, dependencies, tech stack, and health status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, platform engineers, and operators use this skill to inventory services, map service dependencies, identify owners, check health endpoints, and detect service catalog drift across a codebase or organization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented scan commands can expose secrets, dependency details, or ownership information in generated reports.

Mitigation: Run the skill only in a low-privilege, secret-free environment and redact dependency or ownership output before sharing reports.

Risk: Raw Python snippets shown in the skill can execute attacker-controlled code when run on repositories with crafted filenames.

Mitigation: Avoid the raw snippets until filenames are passed as arguments safely or otherwise sanitized.

Risk: Live health checks can contact local services or endpoints.

Mitigation: Run live health checks only with explicit authorization.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Text, Markdown, JSON, and Mermaid reports with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include service inventory, dependency graph, ownership report, drift findings, and optional live health status.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
