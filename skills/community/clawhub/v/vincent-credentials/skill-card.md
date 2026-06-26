## Description: <br>
Secure credential management for agents that need to store API keys, passwords, OAuth tokens, or SSH keys and write them to .env files without exposing values. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[glitch003](https://clawhub.ai/user/glitch003) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when an application needs credentials but the values should stay out of the agent conversation. The skill guides the agent through creating or selecting a Vincent secret and writing selected values into a local .env file through the Vincent CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can use a third-party CLI and service to manage credentials and write them into local .env files. <br>
Mitigation: Install only when the user trusts Vincent/heyvincent.ai for the credentials involved, and require explicit confirmation before running credential or .env write commands. <br>
Risk: A credential may be written to the wrong .env path or committed accidentally. <br>
Mitigation: Verify the target .env path before writing, keep .env files out of git, and rotate any secret that may have been exposed or written incorrectly. <br>
Risk: Using an unpinned CLI can change credential behavior between runs. <br>
Mitigation: Pin or review the @vincentai/cli version before use when operating on sensitive credentials. <br>


## Reference(s): <br>
- [Vincent homepage](https://heyvincent.ai) <br>
- [ClawHub skill page](https://clawhub.ai/glitch003/vincent-credentials) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown with inline bash commands and JSON command output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local .env files and credential CLI configuration paths declared by the skill metadata.] <br>

## Skill Version(s): <br>
1.0.69 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
