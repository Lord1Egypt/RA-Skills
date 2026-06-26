## Description: <br>
Scan trending stocks and crypto movers with live AISA market signals when users ask what is hot, moving, gaining momentum, or news-driven right now. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and market-focused agents use this skill to request live summaries of stock and crypto movers, momentum names, and market catalysts. Outputs are informational only and not financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends finance-related prompts to the configured AISA API provider and requires an AISA_API_KEY. <br>
Mitigation: Install only when this external API use is acceptable and keep the API key in the environment rather than in prompts or files. <br>
Risk: Trigger wording may be broad for requests about what is hot or moving. <br>
Mitigation: Use or configure the skill only for explicit stock, crypto, or market-momentum requests. <br>
Risk: Market summaries can be time-sensitive and should not be treated as investment recommendations. <br>
Mitigation: Keep the informational-only posture visible to users and verify material decisions against authoritative financial sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bibaofeng/stock-hot) <br>
- [AISA API endpoint](https://api.aisa.one/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown report with optional compact JSON summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and can focus on stocks, crypto, or both.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
