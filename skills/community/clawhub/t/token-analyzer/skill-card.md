## Description: <br>
Token Analyzer analyzes crypto token contracts on Solana, BSC, and Base using GMGN data for market metrics, security checks, KOL and developer analysis, and AI-assisted narrative, holder, insider, and bot signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanguang254](https://clawhub.ai/user/hanguang254) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External agents and developers use this skill to query crypto token contract addresses and receive market, safety, holder, KOL, developer, and social-signal analysis for SOL, BSC, and Base tokens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Chrome remote debugging session, which can expose browser state if attached to a normal logged-in profile or left open. <br>
Mitigation: Use a dedicated disposable Chrome profile, bind debugging to localhost, avoid logged-in personal sessions, and close port 9222 after use. <br>
Risk: The skill performs browser automation and enriches results with GMGN and Twitter/X data through bird, with packaged legacy Ave.ai code also present. <br>
Mitigation: Review these data sources and scripts before deployment, and run the skill only in environments where those third-party services and behaviors are acceptable. <br>


## Reference(s): <br>
- [ClawHub Token Analyzer Release Page](https://clawhub.ai/hanguang254/token-analyzer) <br>
- [Publisher Profile](https://clawhub.ai/user/hanguang254) <br>
- [GMGN](https://gmgn.ai) <br>
- [OpenClaw Browser Relay](https://chromewebstore.google.com/detail/openclaw-browser-relay/nglingapjinhecnfejdcpihlpneeadjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables, links, scores, risk labels, and setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports token market data, safety checks, holder concentration, KOL participation, developer history, Twitter/X-derived signals, and AI-assisted risk summaries when the required data sources are available.] <br>

## Skill Version(s): <br>
2.5.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
