## Description: <br>
Use when running SafeFlow against a deployed Solana program to generate an agent keypair, guide owner wallet/session setup, save payment configuration, and execute rate-limited Solana payments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fwangzil](https://clawhub.ai/user/fwangzil) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to prepare a Solana agent wallet, hand setup to the wallet owner, store the returned owner configuration, query session budget, and submit on-chain payments under SafeFlow rate limits and caps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent real Solana spending authority through a locally stored keypair and SafeFlow session. <br>
Mitigation: Use a dedicated low-balance wallet, set strict rate limits and total caps, and revoke or expire sessions when autonomous payment access is no longer needed. <br>
Risk: The local `.safeflow/agent-keypair.json` file can authorize transactions if exposed. <br>
Mitigation: Keep the keypair out of git, backups, and logs; restrict file permissions; and rotate the agent wallet if exposure is suspected. <br>
Risk: A wrong cluster, recipient, or amount can move funds to an unintended destination. <br>
Mitigation: Verify the Solana cluster, recipient address, and amount before every transfer, and add a confirmation or dry-run step before funding production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fwangzil/safe-flow-solana-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and local JSON configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces owner handoff instructions, local keypair/configuration files, session status output, and transaction status messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
