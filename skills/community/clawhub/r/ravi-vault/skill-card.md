## Description: <br>
Store and retrieve key-value secrets — E2E encrypted vault for API keys and env vars. Do NOT use for website passwords (use ravi-passwords) or reading messages (use ravi-inbox). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raunaksingwi](https://clawhub.ai/user/raunaksingwi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use Ravi Vault to store, list, retrieve, and delete API keys, environment variables, and tokens through the Ravi CLI. The skill is intended for runtime access to key-value secrets, not website passwords or message retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stored secrets can be retrieved in plaintext by an agent using the Ravi CLI. <br>
Mitigation: Install and use this skill only when the Ravi CLI and vault service are trusted, and store only secrets that the agent is allowed to access. <br>
Risk: Retrieved secret values can be exposed through logs, terminal output, shell history, or long-lived environment variables. <br>
Mitigation: Avoid printing or logging secret values, pass them directly to the command that needs them, and clear temporary variables after use. <br>
Risk: Secret key names are stored in plaintext for lookup and filtering. <br>
Mitigation: Use descriptive key names that do not themselves contain sensitive values or private context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/raunaksingwi/ravi-vault) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance focuses on Ravi CLI commands that emit JSON for agent parsing.] <br>

## Skill Version(s): <br>
1.6.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
