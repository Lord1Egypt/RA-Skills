## Description: <br>
Search, analyze, and trade on Manifold Markets prediction markets by checking odds, placing bets, viewing portfolios, and managing positions through the Manifold API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[silverstone-louis](https://clawhub.ai/user/silverstone-louis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to inspect Manifold Markets data, review account and portfolio information, and execute user-directed trades with a Manifold API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated commands can place bets, sell shares, or cancel orders using the user's Manifold API key. <br>
Mitigation: Use --dry-run before bets, manually verify contract IDs, amounts, outcomes, and answer IDs, and keep the API key scoped to Manifold. <br>
Risk: A local data/.env file near the skill can load environment variables automatically. <br>
Mitigation: Review or remove any local data/.env file near the skill so unintended variables are not loaded. <br>


## Reference(s): <br>
- [Silke Manifold on ClawHub](https://clawhub.ai/silverstone-louis/silk-manifold) <br>
- [Manifold API endpoint](https://api.manifold.markets/v0) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [JSON from the Manifold CLI, with Markdown usage examples in the skill instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require python3 and MANIFOLD_API_KEY for authenticated Manifold account actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
