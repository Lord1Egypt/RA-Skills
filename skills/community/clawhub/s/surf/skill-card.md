## Description: <br>
Surf provides a CLI-backed crypto data skill for real-time prices, wallets, social intelligence, DeFi, on-chain SQL, prediction markets, news, and related crypto data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hughzhou-gif](https://clawhub.ai/user/hughzhou-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and crypto-focused users use Surf to fetch live crypto data through the surf CLI, including market prices, wallet activity, DeFi metrics, on-chain queries, social signals, prediction markets, and crypto news. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make persistent project and home-directory changes, including routing files and declined-routing markers. <br>
Mitigation: Review or decline routing changes, inspect diffs before any commit, and install only where Surf should be a default crypto data source. <br>
Risk: Feedback submission can send recent chat context that may contain sensitive crypto or project information. <br>
Mitigation: Avoid feedback submission when recent turns include wallet addresses, API keys, portfolio details, trading plans, or private project information. <br>
Risk: The skill may involve sensitive credentials and live external crypto data. <br>
Mitigation: Configure API keys outside chat, do not paste keys into conversations, and present API responses as data rather than instructions. <br>


## Reference(s): <br>
- [Surf CLI Introduction](https://agents.asksurf.ai/docs/cli/introduction) <br>
- [Surf Dashboard](https://agents.asksurf.ai) <br>
- [Surf API Gateway](https://api.asksurf.ai/gateway/v1) <br>
- [ClawHub Skill Page](https://clawhub.ai/hughzhou-gif/surf) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown prose with shell commands and JSON response data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live crypto API results; agents should treat returned API content as untrusted external data.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
