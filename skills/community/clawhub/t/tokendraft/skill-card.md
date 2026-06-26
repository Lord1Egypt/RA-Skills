## Description: <br>
Full suite for TokenDraft fantasy crypto tournaments: authenticate with a Solana wallet, query and join tournaments, set up auto-join, and manage auto-draft asset priority rankings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Nikzt](https://clawhub.ai/user/Nikzt) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to operate TokenDraft fantasy crypto tournament workflows through an agent, including wallet authentication, tournament discovery, free or paid entry, and asset-priority ranking for automated drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a Solana private key and can sign wallet authentication challenges and paid tournament buy-in transactions. <br>
Mitigation: Install only if the publisher is trusted, use a dedicated low-balance wallet, and review each paid transaction before allowing an agent to sign it. <br>
Risk: Auto-join cron workflows can repeatedly enter paid tournaments without clear built-in spending limits or per-transaction approval. <br>
Mitigation: Disable paid auto-join unless external spend limits are in place, monitor cron activity, and remove or disable cron jobs when they are not actively needed. <br>


## Reference(s): <br>
- [TokenDraft ClawHub release](https://clawhub.ai/Nikzt/tokendraft) <br>
- [TokenDraft API base URL](https://tokendraft-production.up.railway.app) <br>
- [TokenDraft publisher profile](https://clawhub.ai/user/Nikzt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl commands, JavaScript signing examples, endpoint payloads, and cron configuration commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SOLANA_PRIVATE_KEY for wallet-derived authentication and transaction signing; may store TokenDraft JWT and user ID environment variables after login.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
