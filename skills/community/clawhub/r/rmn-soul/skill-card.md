## Description: <br>
RMN Soul builds a recursive memory network from an agent workspace, archives memory data through IPFS-compatible storage, and anchors memory integrity metadata to an ERC-8004 identity on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weidadong2359](https://clawhub.ai/user/weidadong2359) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to turn local agent memory files into a layered memory graph, periodically compute integrity proofs, and restore or verify an agent from anchored identity metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles private agent memory and may archive it into rmn-soul-data and IPFS-addressed storage. <br>
Mitigation: Review and redact memory, identity, and issue files before setup or anchoring; use local-only/manual anchoring when permanence or public retrieval is not acceptable. <br>
Risk: On-chain anchoring uses wallet signing and private-key configuration for Base transactions. <br>
Mitigation: Avoid funded private keys until shell execution and transaction behavior are reviewed; prefer a limited-purpose wallet and manual calldata review. <br>
Risk: Restore flows fetch memory data from IPFS gateways and overwrite local rmn-soul-data state. <br>
Mitigation: Verify the expected agent ID, owner, and Merkle root before trusting restored data, and keep a backup of existing local memory files. <br>


## Reference(s): <br>
- [RMN Soul on ClawHub](https://clawhub.ai/weidadong2359/rmn-soul) <br>
- [Publisher profile](https://clawhub.ai/user/weidadong2359) <br>
- [ERC-8004 registration reference](https://eips.ethereum.org/EIPS/eip-8004#registration-v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON configuration and shell commands; scripts produce JSON files, console reports, IPFS references, and on-chain transaction metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update rmn-soul-data files in the workspace and may use local command-line tools for IPFS and Base chain interactions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
