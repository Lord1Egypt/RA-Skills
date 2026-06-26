## Description: <br>
A multi-chain wallet skill for AI agents, with local sandbox signing, secure PIN handling, and configurable risk controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[willjefferson0](https://clawhub.ai/user/willjefferson0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to install and operate a local wallet sandbox, inspect wallet status, and perform signing or transfer workflows with explicit user confirmation. It is intended for AI-agent wallet operations that require local configuration, bearer-token authentication, and user-controlled risk policies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sign transactions and transfer assets through a wallet sandbox. <br>
Mitigation: Confirm every transaction manually and review the requested chain, asset, recipient, and amount before execution. <br>
Risk: The skill depends on local secret files and bearer tokens such as CLAY_AGENT_TOKEN, AGENT_TOKEN, .env.clay, and identity.json. <br>
Mitigation: Treat these values as secrets; do not paste them into chat logs, commit them, or share them with untrusted parties. <br>
Risk: The release uses remote installer and upgrade flows from clawwallet.cc and writes persistent wallet state under skills/claw-wallet. <br>
Mitigation: Install only if the publisher and distribution host are trusted, and review installers or upgrades before running them. <br>


## Reference(s): <br>
- [ClawHub Wallet Listing](https://clawhub.ai/willjefferson0/wallet-test) <br>
- [Claw Wallet Skill Homepage](https://github.com/ClawWallet/Claw-Wallet-Skill) <br>
- [Claw Wallet Skill Distribution Host](https://www.clawwallet.cc/skills) <br>
- [Claw Wallet Site](https://www.clawwallet.cc) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration guidance, API calls, Text] <br>
**Output Format:** [Markdown with inline shell commands and JSON API payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wallet status, addresses, bind URLs, policy guidance, and transaction confirmation prompts.] <br>

## Skill Version(s): <br>
0.1.19 (source: server release metadata and skill.yml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
