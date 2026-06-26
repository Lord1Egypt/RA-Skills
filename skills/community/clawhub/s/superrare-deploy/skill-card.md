## Description: <br>
Deploy a SuperRare Sovereign ERC-721 collection on Ethereum or Base via Bankr. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaigotchi](https://clawhub.ai/user/aaigotchi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare, dry-run, and optionally broadcast SuperRare Sovereign ERC-721 collection deployments through Bankr on Ethereum or Base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broadcast mode can submit a real blockchain deployment transaction. <br>
Mitigation: Run the default dry-run first and verify the chain, factory address, calldata, collection name, and symbol before using --broadcast. <br>
Risk: The skill may use an existing Bankr credential from the environment or local Bankr config. <br>
Mitigation: Install and run it only in an environment where using that Bankr credential is intended. <br>
Risk: Deployment receipt files may include RPC URLs or deployment metadata. <br>
Mitigation: Review receipt JSON files before sharing them outside the deployment team. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aaigotchi/superrare-deploy) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON receipt files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Broadcast deployments can write receipt JSON files containing transaction, RPC, and deployment metadata.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
