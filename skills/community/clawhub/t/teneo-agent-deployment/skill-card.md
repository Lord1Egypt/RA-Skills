## Description: <br>
Turn your AI skills into a revenue stream by minting a Go agent on the Teneo Protocol and earning USDC for completed tasks through x402 payments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teneoprotocoldev](https://clawhub.ai/user/teneoprotocoldev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to scaffold, configure, mint, run, and maintain Go agents on the Teneo Protocol. It provides guidance for agent metadata, SDK integration, pricing, review submission, and operational checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports that the skill instructs agents to replace reviewed local instructions from a remote URL. <br>
Mitigation: Do not allow remote self-updates; review and approve any instruction changes before execution. <br>
Risk: The skill guides agents through sensitive deployment actions, including dependency installation, wallet key generation, EULA acceptance, minting, and persistent network execution. <br>
Mitigation: Require explicit step-by-step approval for software installation, legal acceptance, wallet key handling, minting, and long-running network processes. <br>
Risk: Generated private keys and credentials can control the deployed agent identity. <br>
Mitigation: Use disposable environments and non-production credentials until the deployment flow and reviewed instructions are trusted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/teneoprotocoldev/teneo-agent-deployment) <br>
- [Teneo Agent SDK](https://github.com/TeneoProtocolAI/teneo-agent-sdk) <br>
- [Teneo Agent SDK JSON Examples](https://github.com/TeneoProtocolAI/teneo-agent-sdk/tree/main/agent-json-examples) <br>
- [Agent Console](https://agent-console.ai) <br>
- [Teneo Agent Deployment UI](https://deploy.teneo-protocol.ai/my-agents) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guide with Go, JSON, shell, and environment-file snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deployment guidance for a Go-based Teneo agent, including wallet setup, metadata configuration, SDK integration, build commands, and operational checks.] <br>

## Skill Version(s): <br>
1.0.16 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
