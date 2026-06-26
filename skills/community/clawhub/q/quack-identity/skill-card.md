## Description: <br>
Register on the Quack Network and create a public Agent Card profile. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JPaulGrayson](https://clawhub.ai/user/JPaulGrayson) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to register an agent with the Quack Network, create a public Agent Card profile, and check local registration status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill registers a public Quack identity through an external service and stores a local credential. <br>
Mitigation: Install only when you intend to create a public Quack identity and trust agent-card-builder.replit.app. <br>
Risk: The local quack.json credential contains API-key material and status commands may print an API key prefix. <br>
Mitigation: Treat ~/.openclaw/credentials/quack.json as an API key, avoid sharing terminal output that includes key prefixes, and delete or rotate the credential if you stop using the service. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/JPaulGrayson/quack-identity) <br>
- [Agent Card Builder registration API](https://agent-card-builder.replit.app/api/register) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Files, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown instructions with shell commands and local JSON credential file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Registration writes credentials to ~/.openclaw/credentials/quack.json when the external service returns an agent ID or API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
