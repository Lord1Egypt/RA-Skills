## Description: <br>
AI-powered X/Twitter search for real-time trends, breaking news, sentiment analysis, and social media insights with paid x402 requests on the Base network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TzannetosGiannis](https://clawhub.ai/user/TzannetosGiannis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to search X/Twitter for trends, breaking news, sentiment, hashtags, viral content, and public opinion. The skill is suited for social media intelligence workflows where paid x402 search requests are acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a raw wallet private key for paid x402 searches. <br>
Mitigation: Use a dedicated low-balance Base wallet and avoid reusing a primary wallet private key. <br>
Risk: The private key may be supplied through plaintext environment variables or JSON configuration files. <br>
Mitigation: Prefer secure secret handling where possible, restrict file permissions, and remove local plaintext configuration when it is no longer needed. <br>
Risk: The skill invokes an unpinned third-party npm package to handle paid searches. <br>
Mitigation: Review or pin the npm package before allowing it to handle wallet credentials or spend funds. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TzannetosGiannis/x-search-x402) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text search results and Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paid x402 requests require a Base wallet private key and cost $0.05 USDC per request.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
