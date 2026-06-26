## Description: <br>
Web3 Daily provides a bilingual public Web3 research digest with macro news, KOL sentiment, BTC/ETH market data, and Fear & Greed Index updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexander10011](https://clawhub.ai/user/alexander10011) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to fetch current Web3 and crypto market research digests from a third-party backend when they ask for Web3 news, crypto digests, or compact daily market summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts a third-party backend for crypto market commentary. <br>
Mitigation: Install only when third-party Web3 research is acceptable, and avoid including sensitive personal, wallet, or account information in prompts that invoke it. <br>
Risk: The returned digest may be interpreted as investment or financial advice. <br>
Mitigation: Treat the digest as third-party market research and verify material claims before making trading or investment decisions. <br>
Risk: The skill depends on live HTTPS API availability. <br>
Mitigation: Handle service errors and timeouts by telling users the J4Y service is temporarily unavailable and suggesting a retry. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexander10011/web3-daily) <br>
- [Project homepage](https://github.com/alexander10011/web3-daily) <br>
- [J4Y Backend API](https://j4y-production.up.railway.app) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown digest extracted from a JSON HTTPS API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual English or Chinese output with full and compact digest variants.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release evidence, SKILL.md frontmatter, and claw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
