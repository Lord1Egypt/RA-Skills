## Description:

Deploys production-grade multi-agent fleets in OpenClaw using scripts, cloud deployment templates, routing configuration, shared memory infrastructure, and deployment health checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhinas90](https://clawhub.ai/user/abhinas90)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to scaffold, configure, validate, and deploy OpenClaw multi-agent fleets across local and cloud environments. It is intended for teams moving from a single agent to coordinated agent deployments with shared memory and routing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared memory and cloud gateways may expose agent state too broadly if deployed without authentication or network controls.

Mitigation: Keep the REST memory API bound to localhost unless authentication and network controls are added, and remove unauthenticated public cloud ingress before production use.

Risk: Deployment, cleanup, and reset workflows can alter cloud resources or local agent state.

Mitigation: Run deployment commands in dry-run mode first, review generated configuration, and back up state before reset or cleanup operations.

Risk: Unpinned packages or container images can create supply-chain drift between review and deployment.

Mitigation: Pin package and image versions before production deployment.

Risk: Workflow execution with untrusted filenames can introduce unsafe behavior.

Mitigation: Run workflow definitions and filenames only from trusted, reviewed sources.

## Reference(s):

- [Multi-Agent Architecture Patterns](references/architecture.md)
- [Structured Memory Schemas for Multi-Agent Systems](references/memory-schemas.md)
- [Troubleshooting Multi-Agent Deployment](references/troubleshooting.md)
- [Workflow DAG Templates for Multi-Agent Deployment](references/workflows.md)
- [ClawHub Release Page](https://clawhub.ai/abhinas90/skills/skill-multi-agent-deployment)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, plus Python, shell, YAML, JSON, and Markdown artifact files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes deployment templates for DigitalOcean, AWS, GCP, Azure, and Kubernetes, along with local scripts for setup, routing, memory synchronization, validation, and deployment.]

## Skill Version(s):

1.4.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
