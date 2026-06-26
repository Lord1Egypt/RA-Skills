## Description: <br>
Synapse Layer helps agents configure and use persistent encrypted memory through a Python client or MCP endpoint, including memory storage, recall, cross-agent search, text processing, and trust-score review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rafacpti23](https://clawhub.ai/user/rafacpti23) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add persistent memory to AI agents, test SynapseLayer connectivity, and integrate memory operations with OpenClaw or external MCP clients. It is also useful for reviewing Trust Quotient scores and configuring framework integrations such as LangChain, CrewAI, AutoGen, LlamaIndex, and Semantic Kernel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent memories can be transmitted to and persisted by an external SynapseLayer service while retention, deletion, encryption, and cross-agent isolation controls are under-specified. <br>
Mitigation: Install only when the service is trusted, avoid storing secrets or regulated data until controls are verified, and separate agent IDs by project or trust boundary. <br>
Risk: The skill requires sensitive API credentials for live service access. <br>
Mitigation: Use scoped disposable API keys for testing and rotate or revoke keys if they are exposed. <br>
Risk: The test script prints a truncated API key and writes test memories to the external service. <br>
Mitigation: Avoid running the test script in shared logs and use non-sensitive test content with a disposable key. <br>


## Reference(s): <br>
- [API Reference](references/api.md) <br>
- [Security Details](references/security.md) <br>
- [Framework Integrations](references/integrations.md) <br>
- [Python Client](scripts/synapse_client.py) <br>
- [SynapseLayer MCP endpoint](https://forge.synapselayer.org/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with Python, JSON, and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce HTTP JSON-RPC requests to the SynapseLayer MCP endpoint when the provided client or test script is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
