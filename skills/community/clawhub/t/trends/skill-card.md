## Description: <br>
Helps users install, configure, use, and troubleshoot the trends-skill-tool CLI for token management, trading, wallet queries, rewards, and related errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[milesxyz](https://clawhub.ai/user/milesxyz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and end users use this skill to operate the global npm trends-skill-tool CLI, including installation, wallet setup, read-only account checks, token creation, buy/sell quote flows, reward status, reward claims, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide high-impact wallet transactions, including token creation, buys, sells, and reward claims. <br>
Mitigation: Use a dedicated low-balance wallet, keep per-transaction confirmations enabled, and verify quotes, parameters, and wallet address before any write action. <br>
Risk: Wallet initialization or force overwrite can replace key material the user may still need. <br>
Mitigation: Avoid wallet init --force unless overwrite is intentional, and verify only wallet addresses rather than reading or printing private key files. <br>
Risk: The release depends on an unreviewed global npm CLI for crypto trading workflows. <br>
Mitigation: Review the package before installing or upgrading, install from the documented package name only, and run version/help checks before using trading commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/milesxyz/trends) <br>
- [Install and setup guide](artifact/references/install-and-setup.md) <br>
- [Command recipes](artifact/references/command-recipes.md) <br>
- [Error playbook](artifact/references/error-playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with command blocks and concise operational steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes confirmation gates for write actions and safe handling guidance for wallet credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
