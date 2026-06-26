## Description: <br>
Search the web using SearXNG to retrieve current information, research topics, documentation, fact-checking context, URLs, and ranked results with titles, URLs, and content snippets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noblepayne](https://clawhub.ai/user/noblepayne) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and agent users use this skill to retrieve current web information, documentation, URLs, and fact-checking context through a configured SearXNG instance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documented search script is not included in the artifact. <br>
Mitigation: Before installing, confirm any separately provided scripts/search.clj comes from the same trusted source and matches the documented behavior. <br>
Risk: Search queries may be sent to the configured SearXNG service. <br>
Mitigation: Use a local or trusted SearXNG instance and avoid putting secrets or sensitive private data into search queries. <br>


## Reference(s): <br>
- [SearXNG API Reference](references/api-guide.md) <br>
- [ClawHub release page](https://clawhub.ai/noblepayne/searxng-local-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Formatted text search results with titles, URLs, snippets, scores, and source engines; documentation includes Markdown and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the bb command and a configured SEARXNG_URL environment variable.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
