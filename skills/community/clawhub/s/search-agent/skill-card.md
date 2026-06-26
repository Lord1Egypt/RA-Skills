## Description: <br>
AI-powered search agent that performs intelligent web searches, aggregates results, and provides summarized answers with source citations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hgta23](https://clawhub.ai/user/hgta23) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask research, news, fact-checking, academic, and code-search questions and receive summarized answers with source lists and confidence-style metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may rely on claimed search, summarization, fact-checking, and credibility scoring behavior that the security evidence says is currently placeholder-quality. <br>
Mitigation: Review results manually, avoid sensitive decisions, and require transparent real search providers before production reliance. <br>
Risk: The skill may fetch web content for user queries once real provider logic is added. <br>
Mitigation: Document which providers receive queries, use HTTPS endpoints, and avoid private or sensitive search terms unless data handling is approved. <br>
Risk: License evidence is inconsistent between server metadata and artifact documentation. <br>
Mitigation: Confirm the intended license before distribution or deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hgta23/search-agent) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [package.json](package.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown-style summaries and structured JSON objects with key findings, sources, confidence, related queries, and metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SEARCH_API_KEY according to the documentation; security evidence says the current implementation returns placeholder search results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
