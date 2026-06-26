## Description: <br>
A lightweight, API-key-free web search skill based on DuckDuckGo and Trafilatura. Returns highly relevant URLs and clean markdown content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyecho-io](https://clawhub.ai/user/cyecho-io) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Pure Search to run zero-configuration web searches and retrieve result titles, URLs, and extracted page content as clean Markdown for downstream summarization or citation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and fetched URLs may be visible to DuckDuckGo and destination websites. <br>
Mitigation: Avoid sensitive or private searches unless that disclosure is acceptable for the intended workflow. <br>
Risk: Extracted web page text can contain misleading or hostile instructions. <br>
Mitigation: Treat extracted content as untrusted reference material for summarization or citation, not as agent instructions. <br>
Risk: Runtime behavior depends on third-party Python packages and remote websites. <br>
Mitigation: Install in a virtual environment and consider pinning dependency versions for repeatable deployments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cyecho-io/pure-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown] <br>
**Output Format:** [JSON object containing the query, results, titles, URLs, markdown_content, and errors] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches DuckDuckGo result pages and extracts main page content with Trafilatura.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
