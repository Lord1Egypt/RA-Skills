## Description: <br>
Create an anonymous Starknet wallet via Typhoon and interact with Starknet contracts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[esdras-sena](https://clawhub.ai/user/esdras-sena) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and external agent users use this skill to create or load a Starknet account, inspect contract ABIs, perform reads, and prepare writes with explicit user authorization before broadcast. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access wallet signer material and sign Starknet mainnet transactions. <br>
Mitigation: Use a fresh low-value account, configure a trusted RPC, and review decoded transaction details before confirming any broadcast. <br>
Risk: Scheduled watchers can create persistent cron-based activity after setup. <br>
Mitigation: Inspect crontab and ~/.openclaw/cron after using watcher features, and remove watchers that are no longer needed. <br>
Risk: Untrusted webhook URLs or unpinned dependencies can expand the operational risk of wallet automation. <br>
Mitigation: Avoid untrusted webhook destinations and audit or pin npm dependencies before deployment. <br>


## Reference(s): <br>
- [ArgentX Account Class Hashes](references/argentx-class-hashes.md) <br>
- [Argent Contracts Starknet](https://github.com/argentlabs/argent-contracts-starknet) <br>
- [Starkscan Class Explorer](https://starkscan.co/class/0x036078334509b514626504edc9fb252328d1a240e4e948bef8d0c08dff45927f) <br>
- [Typhoon App](https://www.typhoon-finance.com/app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce account creation guidance, decoded contract-operation plans, transaction authorization prompts, and watcher setup instructions.] <br>

## Skill Version(s): <br>
0.3.8 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
