## Description: <br>
Shodh Local provides local offline cognitive memory for AI agents with semantic recall, GTD todo and project tracking, a knowledge graph, and proactive context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[doobidoo](https://clawhub.ai/user/doobidoo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to connect an agent to a local Shodh-Memory server for persistent recall, todo and project tracking, proactive context, and knowledge graph access across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory can retain and later surface user or project information across agent sessions. <br>
Mitigation: Avoid storing secrets, credentials, health, financial, or other sensitive details unless memory inspection, deletion, and retention controls are clear. <br>
Risk: The skill asks the agent to use an agent-managed local memory server. <br>
Mitigation: Review before installing, keep access limited to localhost, protect the API key, and periodically review or delete stored memory. <br>


## Reference(s): <br>
- [Shodh API Endpoints](reference/api.md) <br>
- [OpenClaw Examples](reference/examples.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/doobidoo/shodh-local) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets a local localhost:3030 Shodh-Memory server with X-API-Key authentication when available.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
