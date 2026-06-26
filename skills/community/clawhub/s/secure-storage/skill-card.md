## Description: <br>
AES encrypted storage for saving sensitive values such as API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amd5](https://clawhub.ai/user/amd5) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set, retrieve, list, and delete locally stored sensitive values from shell commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says the decryption key is embedded in source, so this should not be treated as strong protection for production API keys, valuable credentials, or regulated secrets. <br>
Mitigation: Use it only for low-scope, revocable values unless it is changed to use a per-user secret, OS keychain, or other real key-management mechanism. <br>
Risk: Retrieved secrets can be printed directly in terminal output, where logs or shell history may expose them. <br>
Mitigation: Avoid using the get command in logged terminals and avoid environments where command arguments or output are captured. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/amd5/secure-storage) <br>
- [Publisher profile](https://clawhub.ai/user/amd5) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Command-line text output and local JSON storage file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores encrypted values in a local JSON file and prints retrieved values to the terminal.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
