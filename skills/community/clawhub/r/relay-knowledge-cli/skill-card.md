## Description: <br>
Relay Knowledge CLI guides agents in using the local relay-knowledge CLI for repository indexing, knowledge graph queries, GraphRAG retrieval, code graph navigation, impact analysis, diagnostics, and upgrade checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevetdp](https://clawhub.ai/user/stevetdp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to index local repositories, query code and software graphs, inspect feature flags, run diagnostics, and manage knowledge-map workflows through the relay-knowledge CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to index and query local repositories and maintain local runtime state. <br>
Mitigation: Use scoped repository paths or a temporary RELAY_KNOWLEDGE_HOME for tests, and review install, service, write, and knowledge-map mutation commands before execution. <br>
Risk: Large repository indexing and service workflows can run as durable background tasks. <br>
Mitigation: Inspect status before retrying, let managed services drain active tasks when present, and use bounded worker attempts for queued or retrying tasks. <br>


## Reference(s): <br>
- [Relay Knowledge homepage](https://github.com/coolplayagent/relay-knowledge) <br>
- [ClawHub skill page](https://clawhub.ai/stevetdp/relay-knowledge-cli) <br>
- [CLI workflows](references/cli-workflows.md) <br>
- [Knowledge map workflows](references/knowledge-map-workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON-oriented CLI workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prefers machine-readable JSON command output, scoped repository paths, and temporary RELAY_KNOWLEDGE_HOME for isolated tests.] <br>

## Skill Version(s): <br>
1.1.12 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
