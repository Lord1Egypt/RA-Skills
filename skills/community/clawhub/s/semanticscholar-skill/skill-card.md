## Description: <br>
Search academic papers, look up citations, find authors, and get paper recommendations using the Semantic Scholar API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agents365-ai](https://clawhub.ai/user/agents365-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and developers use this skill to search Semantic Scholar, traverse citation graphs, find authors, get related-paper recommendations, and export literature results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Academic search queries, paper identifiers, and author lookups are sent to Semantic Scholar. <br>
Mitigation: Use an appropriate S2_API_KEY, avoid confidential research topics without approval, and review queries before execution. <br>
Risk: Export functions can save BibTeX, Markdown, or JSON result files locally. <br>
Mitigation: Export only when local files are intended, and review saved results before sharing or relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agents365-ai/semanticscholar-skill) <br>
- [Semantic Scholar API documentation](https://api.semanticscholar.org/api-docs/) <br>
- [Semantic Scholar API key information](https://www.semanticscholar.org/product/api#api-key) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, tables, Python scripts, shell commands, and optional BibTeX, Markdown, or JSON exports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a single-script workflow with built-in rate limiting and retries; S2_API_KEY is optional for higher rate limits.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
