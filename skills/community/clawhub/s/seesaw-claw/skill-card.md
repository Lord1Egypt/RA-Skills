## Description: <br>
SeeSaw Claw integrates SeeSaw prediction-market APIs into OpenClaw so agents can list markets, get quotes, trade positions, check balances, and manage market activity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seesaw](https://clawhub.ai/user/seesaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to connect an agent to SeeSaw prediction markets for account review, market discovery, quote retrieval, trading, settlement, social actions, and market-management workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make live financial and public account actions with SeeSaw credentials. <br>
Mitigation: Start with dry_run enabled, review proposed actions before live execution, and avoid unattended automation unless live trading or market changes are intended. <br>
Risk: Configured integrations may share data with Brave, Gemini, or Slack. <br>
Mitigation: Only configure third-party API keys approved for the deployment and avoid sending sensitive account, credential, or private trading information through prompts or notifications. <br>
Risk: The security evidence flags the token cache in /tmp as a credential-risk item. <br>
Mitigation: Monitor or replace the token-cache behavior before production use, restrict host access, and rotate SeeSaw credentials if token exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/seesaw/seesaw-claw) <br>
- [SeeSaw application](https://app.seesaw.fun) <br>
- [SeeSaw API base URL](https://app.seesaw.fun/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls] <br>
**Output Format:** [CLI text or JSON responses, Markdown usage guidance, shell commands, and OpenClaw configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Automation scripts support dry-run paths; live runs can call SeeSaw APIs and configured Brave, Gemini, or Slack integrations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
