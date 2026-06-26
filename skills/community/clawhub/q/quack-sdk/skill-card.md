## Description: <br>
Developer toolkit for connecting any AI agent to the Quack Network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JPaulGrayson](https://clawhub.ai/user/JPaulGrayson) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to connect agents to the Quack Network, register agent identities, send messages, and consult the Quack API reference. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The quickstart performs live Quack Network registration and sends a real test message. <br>
Mitigation: Review the command before execution and run it only when live network actions are intended. <br>
Risk: The quickstart persists an API key and private key under ~/.openclaw/credentials/quack.json. <br>
Mitigation: Restrict permissions on the credentials file and rotate credentials if the file may have been exposed. <br>
Risk: The skill depends on an external Quack service and publisher trust. <br>
Mitigation: Install and run it only if the publisher and Quack service are trusted for the intended environment. <br>


## Reference(s): <br>
- [Quack Network API Reference](references/api.md) <br>
- [Quack Network API](https://quack.us.com) <br>
- [Quack SDK Interactive Playground](https://quack-assets.replit.app) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to run a Node.js quickstart that registers an agent, sends a test message, and writes local credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
