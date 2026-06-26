## Description: <br>
Scan M&A, insider, analyst, social, and regulatory rumor signals through AISA. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aisadocs](https://clawhub.ai/user/aisadocs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to scan early market signals, including M&A chatter, insider activity, analyst changes, social signals, and regulatory activity. Outputs should be treated as leads for further review, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market-rumor outputs can be incomplete, unconfirmed, or misleading if treated as financial advice. <br>
Mitigation: Use outputs only as leads and verify every signal against primary sources before acting. <br>
Risk: The skill sends market-analysis prompts through an AISA-compatible API using AISA_API_KEY. <br>
Mitigation: Install only if you trust the AISA API provider and avoid sending sensitive information beyond the intended market-analysis request. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aisadocs/stock-rumors-aisa) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown report with an optional compact JSON summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and python3; supports focus filters for all signals, M&A, insider activity, analyst actions, and social signals.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
