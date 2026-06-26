## Description: <br>
Xyz provides web search for agents across DuckDuckGo, Tavily, Bing, Google, and SearXNG, returning structured search results with titles, links, and snippets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jwu26](https://clawhub.ai/user/jwu26) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and agent users use Xyz to search current web information and collect structured evidence for research, market analysis, product research, and technical investigation tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and provider requests may leave the user's machine. <br>
Mitigation: Avoid submitting secrets, private customer data, or regulated information unless that external transmission is acceptable. <br>
Risk: External search provider credentials may be over-permissioned or exposed if configured carelessly. <br>
Mitigation: Use limited API keys and configure only the providers required for the task. <br>
Risk: A SearXNG configuration can route searches through an untrusted instance. <br>
Mitigation: Configure SearXNG only to a trusted instance before using that backend. <br>
Risk: The documentation and artifact disagree about the script entry point. <br>
Mitigation: Confirm the correct script path before execution. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text, Markdown reports, or JSON search-result objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Searches may contact external providers; optional API keys enable Tavily, Bing, Google, and SearXNG backends.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
