## Description: <br>
AI Agent cluster orchestration platform - manage, schedule, and coordinate multiple AI agents locally with FastAPI backend and React dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZhenStaff](https://clawhub.ai/user/ZhenStaff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to set up and operate a local multi-agent orchestration environment with an agent registry, task queue, dashboard, and REST API control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing or running the referenced package or source may execute local services and dependencies that should be reviewed first. <br>
Mitigation: Review the package or repository before installation and prefer Docker or another isolated environment for first runs. <br>
Risk: The local dashboard, API, and Redis services can expose data or control surfaces if bound beyond localhost. <br>
Mitigation: Keep ports bound to localhost, use firewall rules for local services, and enable stronger deployment controls before exposing the system. <br>
Risk: Optional LLM API keys could be exposed or used unexpectedly if configured broadly. <br>
Mitigation: Add OpenAI or Anthropic API keys only when needed, store them in a protected environment file, and do not commit secrets. <br>
Risk: Tool and custom agents may run scripts, modify files, access accounts, or call external systems. <br>
Mitigation: Require human approval and sandboxing for tool or custom agents that can affect files, credentials, accounts, or external services. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ZhenStaff/swarm-orchestrator) <br>
- [Artifact README](artifact/readme.md) <br>
- [Artifact skill definition](artifact/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands, configuration examples, and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local setup, verification, usage, and safety guidance for the orchestration environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
