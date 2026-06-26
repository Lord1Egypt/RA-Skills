## Description: <br>
The Instagram Agent allows agents to retrieve public Instagram profile, post, hashtag, and comment data through the Teneo SDK. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teneoprotocoldev](https://clawhub.ai/user/teneoprotocoldev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Businesses, researchers, and developers use this skill to query public Instagram profiles, posts, hashtags, and comments for market trend, competitor, and community sentiment analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet private keys and USDC payment setup can expose funds if a primary wallet or seed phrase is used. <br>
Mitigation: Use a dedicated low-balance wallet, never provide a primary wallet or seed phrase, and verify the Teneo SDK package and endpoints before use. <br>
Risk: Automatic paid Instagram queries can incur unintended USDC charges. <br>
Mitigation: Require explicit approval and a spending limit before any paid Instagram query. <br>
Risk: Collection of public Instagram data may create compliance or platform-policy obligations. <br>
Mitigation: Limit use to public information and confirm the planned data use complies with applicable regulations, platform terms, and research ethics. <br>


## Reference(s): <br>
- [Instagram Agent on ClawHub](https://clawhub.ai/teneoprotocoldev/teneo-agent-instagram-agent) <br>
- [Teneo Agent SDK on ClawHub](https://clawhub.ai/teneoprotocoldev/teneo-agent-sdk) <br>
- [Teneo SDK npm Package](https://www.npmjs.com/package/@teneo-protocol/sdk) <br>
- [Teneo Protocol](https://teneo-protocol.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript and shell command examples; agent responses may include formatted text or raw structured data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Teneo SDK access, wallet authentication, USDC payments, and a supported payment network; command scope and volume are user-specified.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
