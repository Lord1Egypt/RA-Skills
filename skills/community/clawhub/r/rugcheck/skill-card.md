## Description: <br>
Analyze Solana tokens for rug pull risks using the RugCheck API, including token safety, risk score, liquidity, holder distribution, metadata mutability, insider patterns, and token discovery signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PsychoTechV4](https://clawhub.ai/user/PsychoTechV4) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to query RugCheck for Solana token risk summaries, detailed reports, holder and liquidity signals, insider graph data, and token discovery lists. Results support token due diligence and should be treated as one risk signal rather than financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries send public Solana mint addresses and token-discovery requests to RugCheck. <br>
Mitigation: Do not submit sensitive private data; verify token addresses before querying external RugCheck endpoints. <br>
Risk: Token risk output can be incomplete or misleading if treated as investment advice. <br>
Mitigation: Present RugCheck results as one due-diligence signal and encourage independent verification before acting. <br>


## Reference(s): <br>
- [ClawHub RugCheck skill page](https://clawhub.ai/PsychoTechV4/rugcheck) <br>
- [PsychoTechV4 ClawHub publisher profile](https://clawhub.ai/user/PsychoTechV4) <br>
- [RugCheck API](https://api.rugcheck.xyz) <br>
- [RugCheck token pages](https://rugcheck.xyz/tokens/<mint>) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries RugCheck read endpoints and pretty-prints JSON responses when possible.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
