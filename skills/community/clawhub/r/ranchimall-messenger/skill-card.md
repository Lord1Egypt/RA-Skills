## Description: <br>
Provides command-line workflows for FLO blockchain messaging, contacts, mail, groups, public-key lookup, FLO and token transfers, transaction history, multisig operations, Bitcoin queries, cryptographic utilities, and local key-value storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[void-57](https://clawhub.ai/user/void-57) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate a decentralized FLO messenger and related blockchain utilities from an agent workflow. It can read and send messages, manage local contacts and groups, query balances and history, and initiate real FLO, token, multisig, or pre-signed Bitcoin broadcast operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles wallet secrets and requires FLO_PRIVATE_KEY for most FLO messenger and transaction operations. <br>
Mitigation: Set wallet keys only through secure environment variables, never paste private keys into chat, and use a dedicated low-value wallet until the reported secret-handling issues are fixed. <br>
Risk: FLO, FLO token, and multisig send actions can move funds or write public on-chain data irreversibly. <br>
Mitigation: Review recipient addresses, amounts, token names, memos, and transaction intent before approving any send, bulk transfer, multisig, broadcast, or destructive storage command. <br>
Risk: The security summary reports unsafe logging, command-line secret handling, plaintext group-key cache, and broadcast confirmation gaps. <br>
Mitigation: Avoid production keys or real funds for sensitive workflows until those gaps are remediated, and inspect local cache files and command output for exposed secrets. <br>


## Reference(s): <br>
- [RanchiMall Messenger on ClawHub](https://clawhub.ai/void-57/ranchimall-messenger) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown with command examples, transaction or query results, and local JSON file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some actions require FLO_PRIVATE_KEY and may create or update contacts.json, groups_cache.json, multisig_cache.json, or idb_data JSON files.] <br>

## Skill Version(s): <br>
1.0.21 (source: server release metadata; package.json reports 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
