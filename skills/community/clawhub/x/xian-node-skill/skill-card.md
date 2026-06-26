## Description: <br>
Set up and manage Xian blockchain nodes for mainnet or testnet deployment, custom network creation, and ongoing node operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Endogen](https://clawhub.ai/user/Endogen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and node operators use this skill to deploy and configure Xian blockchain nodes, create custom networks, monitor node status, and troubleshoot common node operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Validator private keys may be exposed through chat, terminal history, logs, or generated output. <br>
Mitigation: Treat validator private keys as secrets; avoid pasting them into chat or command history, store them in a protected file or secret manager, and back them up securely. <br>
Risk: Reset and wipe commands can remove node data or disrupt a running validator or service node. <br>
Mitigation: Review each reset command before execution and back up node keys, genesis files, and configuration before using wipe or full reset workflows. <br>
Risk: Incorrect node, seed, genesis, or validator configuration can prevent syncing or create an unintended network state. <br>
Mitigation: Verify network, seed node, genesis file, moniker, port, and validator settings against the intended Xian network before starting or restarting the node. <br>


## Reference(s): <br>
- [Xian Node ClawHub page](https://clawhub.ai/Endogen/xian-node-skill) <br>
- [Genesis File Template](references/genesis-template.md) <br>
- [xian-network/xian-stack](https://github.com/xian-network/xian-stack) <br>
- [xian-network/xian-core](https://github.com/xian-network/xian-core) <br>
- [xian-network/xian-py](https://github.com/xian-network/xian-py) <br>
- [CometBFT docs](https://docs.cometbft.com/) <br>
- [Xian project site](https://xian.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands, configuration examples, JSON snippets, and Python helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce validator key material, genesis configuration entries, node status summaries, and operational troubleshooting guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
