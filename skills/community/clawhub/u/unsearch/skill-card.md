## Description: <br>
Search the web, scrape content, and conduct deep research using the UnSearch API for real-time search results, URL content extraction, fact verification, and multi-source research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Rakesh1002](https://clawhub.ai/user/Rakesh1002) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and agent builders use this skill to give agents guidance for calling the UnSearch API for web search, content extraction, deep research, and fact verification. It is intended for workflows that need current web information or source-backed research responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, claims, URLs, and extraction requests are sent to the third-party UnSearch service. <br>
Mitigation: Do not submit secrets, regulated data, internal-only URLs, pre-signed links, or confidential business prompts unless policy allows it and the provider is trusted. <br>
Risk: The UnSearch API key can be exposed if copied into prompts, logs, repositories, or shared configuration. <br>
Mitigation: Store UNSEARCH_API_KEY securely, avoid embedding it in shared artifacts, and rotate it immediately if exposed. <br>


## Reference(s): <br>
- [UnSearch Homepage](https://unsearch.dev) <br>
- [UnSearch Documentation](https://docs.unsearch.dev) <br>
- [UnSearch API Reference](https://docs.unsearch.dev/api) <br>
- [ClawHub Skill Page](https://clawhub.ai/Rakesh1002/unsearch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON, bash, Python, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires UNSEARCH_API_KEY for API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
