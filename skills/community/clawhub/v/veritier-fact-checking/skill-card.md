## Description: <br>
Extracts falsifiable claims from text or documents and verifies them against live web evidence or approved private references through Veritier's remote MCP and REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[salomonhenao](https://clawhub.ai/user/salomonhenao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, media teams, and AI agent operators use this skill to extract falsifiable claims from text or URL documents and verify them against web evidence or approved private references before publishing or relying on content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted text, document URLs, and private references are processed by Veritier. <br>
Mitigation: Only submit content approved for external processing; avoid secrets, regulated data, signed/internal URLs, and proprietary documents unless organizational policy allows it. <br>
Risk: The integration requires an API key for live MCP or REST API use. <br>
Mitigation: Use scoped, revocable keys; use test keys for integration testing; send production keys only to https://api.veritier.ai. <br>
Risk: Running the provided example code in production introduces dependency and operational risk. <br>
Mitigation: Pin and audit dependencies, keep webhook secrets separate from API keys, and verify webhook signatures before trusting delivered results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/salomonhenao/veritier-fact-checking) <br>
- [Publisher profile](https://clawhub.ai/user/salomonhenao) <br>
- [Veritier documentation](https://veritier.ai/docs) <br>
- [Veritier website](https://veritier.ai) <br>
- [Veritier dashboard](https://veritier.ai/dashboard) <br>
- [Veritier MCP endpoint](https://api.veritier.ai/mcp/) <br>
- [Veritier API base](https://api.veritier.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-like tool results with claim verdicts, confidence scores, explanations, source URLs, setup commands, and configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require VERITIER_API_KEY for live API or MCP use; test scripts can use VERITIER_TEST_KEY, and webhook examples can use VERITIER_WEBHOOK_SECRET.] <br>

## Skill Version(s): <br>
2.1.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
