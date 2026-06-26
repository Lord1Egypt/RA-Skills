## Description: <br>
Store and retrieve key-value secrets in Ravi for API keys, environment variables, and tokens, rather than website passwords or messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raunaksingwi](https://clawhub.ai/user/raunaksingwi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to manage Ravi CLI secrets: store, list, retrieve, and delete API keys, environment variables, or tokens at runtime. It is intended for key-value secrets, not website passwords or message retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally handles API keys and tokens, and Ravi returns plaintext values to the agent. <br>
Mitigation: Install only if you trust the Ravi CLI and service, use least-privilege credentials, retrieve only specific secrets when needed, and avoid printing or logging secret values. <br>
Risk: Deleting secrets by UUID can remove the wrong secret if the identifier is mistaken. <br>
Mitigation: Carefully verify UUIDs before deleting secrets. <br>
Risk: Secret key names are stored in plaintext for lookup and filtering. <br>
Mitigation: Use descriptive but non-sensitive key names, and keep sensitive material in encrypted values or notes. <br>


## Reference(s): <br>
- [Ravi Secrets API Reference](https://ravi.id/docs/schema/secrets.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown with bash commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May retrieve plaintext secret values; avoid logging or sharing returned values.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
