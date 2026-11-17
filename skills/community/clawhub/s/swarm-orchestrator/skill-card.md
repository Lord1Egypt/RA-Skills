## Description:

AI Agent cluster orchestration platform that helps developers manage, schedule, and coordinate multiple AI agents locally with a FastAPI backend and React dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up and operate a local multi-agent orchestration stack, including agent registration, task queues, monitoring, and REST API control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install instructions pull and run unpinned external code with broad local privileges.

Mitigation: Review the referenced repository and package contents, pin to a full verified commit or signed release, and install in an isolated environment.

Risk: Global npm installation and elevated execution can increase local system exposure.

Mitigation: Avoid running as root and avoid global npm installation where possible.

Risk: Dashboard and API ports may expose local orchestration controls if bound beyond localhost.

Mitigation: Keep ports bound to localhost and restrict external access with firewall or deployment configuration.

Risk: Optional OpenAI or Anthropic API keys can send selected agent prompts or task data to external LLM providers.

Mitigation: Provide API keys only when intentionally enabling LLM agents and store secrets in a protected local environment file.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhenstaff/skills/swarm-orchestrator)
- [Artifact-declared GitHub Repository](https://github.com/ZhenRobotics/openclaw-swarm-orchestrator)
- [Artifact-declared README](https://github.com/ZhenRobotics/openclaw-swarm-orchestrator/blob/main/README.md)
- [Artifact-declared Quickstart](https://github.com/ZhenRobotics/openclaw-swarm-orchestrator/blob/main/QUICKSTART.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, configuration snippets, API examples, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers local setup, service configuration, agent and task API examples, and security practices.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
