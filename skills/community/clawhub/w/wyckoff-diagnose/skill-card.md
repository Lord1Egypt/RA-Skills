## Description: <br>
Wyckoff Diagnose analyzes Chinese A-share stock codes with Wyckoff phase detection, volume profile levels, scoring, ratings, and left-side accumulation or right-side trend perspectives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dxarch1980](https://clawhub.ai/user/dxarch1980) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to generate technical stock-analysis reports for 6-digit A-share codes, including Wyckoff phase, volume profile support and resistance levels, ratings, and operational guidance. The output should be treated as informational analysis rather than investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock codes may be sent to multiple external data providers, including an undocumented non-HTTPS endpoint. <br>
Mitigation: Review data-provider behavior before installation and prefer a version that discloses all providers and uses HTTPS endpoints. <br>
Risk: The skill uses an embedded credential for market-data access. <br>
Mitigation: Prefer a version that removes embedded credentials and requires users to provide their own API token explicitly. <br>
Risk: Generated reports include buy/sell-style guidance that can be mistaken for investment advice. <br>
Mitigation: Treat reports as informational technical analysis and require human financial review before trading decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dxarch1980/wyckoff-diagnose) <br>
- [Publisher profile](https://clawhub.ai/user/dxarch1980) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown-style stock diagnosis report with command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include market-data-derived ratings, key price levels, green and red flags, and buy/sell-style guidance.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
