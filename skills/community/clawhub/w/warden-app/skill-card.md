## Description: <br>
Use the Warden App agentic wallet through browser automation for swaps, bridges, deposits and withdrawals, perps, portfolio review, research, and repeatable workflow documentation with explicit confirmation gates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deiu](https://clawhub.ai/user/deiu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to operate Warden wallet workflows in a browser, inspect balances or positions, and prepare transactions that require explicit user approval before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide high-impact crypto wallet actions such as swaps, bridges, deposits, withdrawals, and perps. <br>
Mitigation: Verify the Warden URL independently, review chain, token, amount, slippage, fees, leverage, and liquidation risk, and only approve execution when the user explicitly intends the transaction. <br>
Risk: Wallet workflows may expose sensitive secrets or private account data if handled carelessly. <br>
Mitigation: Never request or store seed phrases or private keys, avoid revealing local files, credentials, IPs, or internal logs, and prefer read-only actions until execution is explicitly authorized. <br>


## Reference(s): <br>
- [Warden App UI Notes](references/warden-ui-notes.md) <br>
- [Warden App](https://app.wardenprotocol.org/) <br>
- [ClawHub release page](https://clawhub.ai/deiu/warden-app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with browser automation steps, confirmation checklists, and optional code or shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should preserve explicit transaction approval gates and avoid requesting or exposing seed phrases, private keys, credentials, or local private data.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
