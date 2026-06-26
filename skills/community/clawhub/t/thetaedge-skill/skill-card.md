## Description: <br>
ThetaEdge is an Options Intelligence Platform skill that lets agents use the Thetix API for finance, investing, trading, portfolio analysis, market data, dashboard widgets, options opportunities, brokerage accounts, and trading ideas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mempko](https://clawhub.ai/user/mempko) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to connect a ThetaEdge account to conversational portfolio analysis, options strategy screening, dashboard card creation, brokerage account lookup, and AI-generated trading idea review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send financial prompts, account IDs, positions, transactions, portfolio context, and strategy details to ThetaEdge. <br>
Mitigation: Install only when the user intends to connect a ThetaEdge account, treat the ThetaEdge API key as a sensitive financial credential, and keep credential files out of source control and sync tools. <br>
Risk: The security guidance calls out under-scoped trade-action and execute-style behavior for opportunity requests. <br>
Mitigation: Require explicit human review before any opportunity act request or execute-style financial action. <br>
Risk: The VM setup, SSH agent forwarding, and tunnel helper can expose development environment access if used carelessly. <br>
Mitigation: Use those helpers only in trusted, short-lived development environments and follow the documented isolation controls. <br>


## Reference(s): <br>
- [Thetix API Reference](reference.md) <br>
- [OpenClaw VM Setup Guide](docs/vm-setup.md) <br>
- [ClawHub skill page](https://clawhub.ai/mempko/thetaedge-skill) <br>
- [Publisher profile](https://clawhub.ai/user/mempko) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl command examples, JSON configuration snippets, and summarized API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires THETAEDGE_API_KEY and can use THETAEDGE_API_BASE to target the ThetaEdge API service.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
