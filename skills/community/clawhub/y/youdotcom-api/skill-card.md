## Description: <br>
Integrate You.com APIs for research, search, and contents into any language using direct HTTP calls with no SDK required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EdwardIrby](https://clawhub.ai/user/EdwardIrby) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to integrate You.com Research, Search, and Contents APIs through standard HTTP clients. It supports building cited research answers, custom search pipelines, content extraction flows, and web-grounded application features. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys can be exposed if copied into source code, logs, or committed configuration. <br>
Mitigation: Store YDC_API_KEY in environment variables or secret storage and avoid committing credentials. <br>
Risk: Returned web content may contain untrusted or misleading data, including HTML or text intended to influence an agent. <br>
Mitigation: Treat API responses as data, sanitize HTML before rendering, avoid executing returned code, and verify citations for high-stakes use cases. <br>
Risk: Generated integration code may install dependencies or make outbound network calls. <br>
Mitigation: Review generated code and dependency install commands before running them in a development or production environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/EdwardIrby/youdotcom-api) <br>
- [You.com Platform](https://you.com/platform) <br>
- [You.com Search Operators](https://docs.you.com/search/search-operators) <br>
- [Search API Input Schema](assets/search.input.schema.json) <br>
- [Research API Input Schema](assets/research.input.schema.json) <br>
- [Contents API Input Schema](assets/contents.input.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JSON schemas and inline TypeScript, Python, and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces direct HTTP integration guidance for You.com Research, Search, and Contents APIs; requires YDC_API_KEY for runtime API calls.] <br>

## Skill Version(s): <br>
3.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
