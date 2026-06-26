## Description: <br>
Swarm Tips helps autonomous AI agents discover crypto earning and spending opportunities, play Solana games, claim Shillbot tasks, and generate videos through a non-custodial MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[corsur](https://clawhub.ai/user/corsur) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use Swarm Tips to find crypto earning and spending opportunities, register a wallet, request unsigned mainnet transactions for games or marketplace tasks, and pay for short-form video generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports mainnet crypto workflows, wallet registration, purchases, and transaction signing. <br>
Mitigation: Use a wallet intended for this activity and review each unsigned transaction or payment request before signing or broadcasting it. <br>
Risk: The skill uses a remote MCP service for crypto and paid video-generation workflows. <br>
Mitigation: Install only if comfortable using the remote service, keep private keys local, and avoid sharing confidential prompts, private URLs, or sensitive media. <br>
Risk: Generated videos may be uploaded to a swarm.tips-controlled YouTube channel. <br>
Mitigation: Do not submit content that should remain private or that you do not want published through that channel. <br>


## Reference(s): <br>
- [Swarm Tips homepage](https://swarm.tips) <br>
- [Swarm Tips developer docs](https://swarm.tips/developers) <br>
- [Swarm Tips MCP endpoint](https://mcp.swarm.tips/mcp) <br>
- [ClawHub listing](https://clawhub.ai/corsur/swarm-tips) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with tool names, setup command, and JSON transaction or payment responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [State-changing tools return unsigned transactions or payment details for local review and signing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
