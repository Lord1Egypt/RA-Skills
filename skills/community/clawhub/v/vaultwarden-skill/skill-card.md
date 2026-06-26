## Description: <br>
Manage Vaultwarden secrets with wrapper scripts for session handling, caching, logging, and scoped read/write operations in collections or personal vaults. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mbojer](https://clawhub.ai/user/mbojer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to authenticate to a configured Vaultwarden server and read, create, update, delete, or rotate vault items through controlled shell wrappers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify Vaultwarden secrets, including broader vault contents when personal-vault fallback is active. <br>
Mitigation: Install only for agents that are allowed to access the target vault, configure a trusted Vaultwarden server, and set VW_COLLECTION_ID explicitly for organization vaults. <br>
Risk: Cached sessions and read results can extend access beyond a single command. <br>
Mitigation: Consider setting VW_CACHE_TTL=0 for sensitive workflows and run vw-lock.sh when work is complete. <br>
Risk: Update, delete, and password rotation commands can change or remove vault data. <br>
Mitigation: Require human approval before running write, delete, or rotation scripts, and verify item IDs before destructive operations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mbojer/vaultwarden-skill) <br>
- [Publisher Profile](https://clawhub.ai/user/mbojer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command examples and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May output secret values when read or rotation scripts are invoked; status and audit details are emitted separately where supported.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
