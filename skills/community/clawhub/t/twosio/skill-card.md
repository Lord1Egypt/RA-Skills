## Description: <br>
575+ pay-per-call agent tools: most data of any x402 API, AI gateway, storage/queues/watchers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[josho](https://clawhub.ai/user/josho) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Twosio to route suitable tasks to 2s.io's pay-per-call APIs for live data, AI gateway calls, storage, queues, schedules, pub/sub, and watcher workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make USDC-billed calls through 2s.io. <br>
Mitigation: Use trial mode before paying, review quoted prices before each paid call, and use a separate low-balance wallet. <br>
Risk: The skill requires an EVM private key for paid Base wallet calls. <br>
Mitigation: Store EVM_PRIVATE_KEY only in secret storage and avoid exposing it in prompts, logs, or checked-in files. <br>
Risk: Stored data, scheduled jobs, or webhook watchers may create persistent effects. <br>
Mitigation: Require explicit user confirmation before storing data, scheduling jobs, or creating webhook watchers. <br>


## Reference(s): <br>
- [Twosio on ClawHub](https://clawhub.ai/josho/skills/twosio) <br>
- [2s.io homepage](https://2s.io) <br>
- [2s.io API directory](https://2s.io/api/directory) <br>
- [2s.io OpenAPI specification](https://2s.io/api/openapi) <br>
- [2s.io MCP endpoint](https://2s.io/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with command snippets, code examples, and API usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to use x402-paid API calls, trial calls, or MCP tools depending on user intent.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
