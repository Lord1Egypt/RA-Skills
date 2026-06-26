## Description: <br>
SEVO is an agent software-delivery pipeline that guides requirements, gates, test authoring, architecture contracts, implementation, independent review, regression, release, verification, and delivery ledger work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuchangxu1989-openclaw](https://clawhub.ai/user/yuchangxu1989-openclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent teams use SEVO to route software work through structured specification, review, implementation, verification, deployment, and delivery-record stages. It is intended to improve traceability and quality gates for AI-agent-assisted software delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release can alter OpenClaw configuration, register hooks, keep pipeline state, dispatch agents, and manage project release workflows. <br>
Mitigation: Install only in workspaces where those actions are allowed, review init and postinstall behavior, and start with guide, off, demo, or dry-run modes before enabling automation. <br>
Risk: Automatic repair loops, scheduled scans, and publish or deploy actions can affect project state or external release targets. <br>
Mitigation: Disable scheduled scans unless wanted, avoid production publish credentials until approval gates and rollback behavior are clear, and review target scopes and retention settings before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuchangxu1989-openclaw/sevo) <br>
- [SEVO website](https://agentos.site/sevo.html) <br>
- [README](README.md) <br>
- [Architecture documentation](docs/architecture.md) <br>
- [Product requirements](docs/product-requirements.md) <br>
- [Standalone integration guide](docs/standalone-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline commands and structured project or pipeline artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initialize OpenClaw configuration, maintain pipeline state, dispatch agents, and manage release workflows when enabled.] <br>

## Skill Version(s): <br>
1.13.1 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
