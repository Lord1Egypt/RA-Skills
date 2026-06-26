## Description: <br>
Helps developers build Towns Protocol bots with SDK setup, slash commands, message handlers, reactions, interactive components, blockchain operations, and deployment guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andreyz](https://clawhub.ai/user/andreyz) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to build and operate Towns Protocol bots, including SDK initialization, event handlers, messaging behavior, interactive forms, blockchain transaction verification, and deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bot credentials, webhook secrets, RPC keys, and funded gas wallets can expose production access or funds if mishandled. <br>
Mitigation: Store APP_PRIVATE_DATA, JWT_SECRET, RPC keys, and wallet material as production secrets; do not commit them; rotate secrets and revoke webhooks when retiring a bot. <br>
Risk: Blockchain actions may transfer value or grant access based on incomplete transaction evidence. <br>
Mitigation: Keep bot permissions and funded balances minimal, and verify on-chain transaction receipts show success before granting access or treating a payment as complete. <br>
Risk: Message-body logs can expose user content outside local development. <br>
Mitigation: Redact or disable message-body logging in non-local environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/andreyz/towns-protocol) <br>
- [Towns Bot Documentation](https://docs.towns.com/build/bots) <br>
- [Towns Developer Portal](https://app.towns.com/developer) <br>
- [@towns-protocol/bot SDK](https://www.npmjs.com/package/@towns-protocol/bot) <br>
- [Messaging API](references/MESSAGING.md) <br>
- [Blockchain Operations](references/BLOCKCHAIN.md) <br>
- [Interactive Components](references/INTERACTIVE.md) <br>
- [Deployment](references/DEPLOYMENT.md) <br>
- [Debugging](references/DEBUGGING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with TypeScript, bash, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are advisory guidance for a developer agent and should be reviewed before running generated commands or deploying bot code.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
