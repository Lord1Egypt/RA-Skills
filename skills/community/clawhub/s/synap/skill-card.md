## Description: <br>
Sovereign AI knowledge infrastructure with typed entity graphs, documents, long-term memory, messaging relay, and AI governance backed by PostgreSQL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antoinesrvt](https://clawhub.ai/user/antoinesrvt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Synap to connect an agent to persistent structured memory, knowledge graph records, documents, and governed message relay workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Synap API key grants access to knowledge-memory and relay operations. <br>
Mitigation: Use least-privilege API keys, keep keys out of logs and source control, and rotate keys if exposed. <br>
Risk: Connected messaging channels may contain sensitive participant messages. <br>
Mitigation: Connect only channels whose participants are allowed to have messages stored and processed by Synap. <br>
Risk: A managed or self-hosted pod becomes the system of record for stored memory and documents. <br>
Mitigation: Install only when the configured Synap pod is trusted, or self-host the pod in an environment the user controls. <br>


## Reference(s): <br>
- [Synap OpenClaw Homepage](https://synap.live/openclaw) <br>
- [Synap](https://synap.live) <br>
- [Hub Protocol Documentation](https://synap.live/docs/hub-protocol) <br>
- [ClawHub Skill Page](https://clawhub.ai/antoinesrvt/synap) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline HTTP examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update records in a configured Synap pod through governed API requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
