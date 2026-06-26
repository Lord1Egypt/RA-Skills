## Description: <br>
smart-research performs multi-engine public web search and fallback page fetching to return structured research results without API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xx235300](https://clawhub.ai/user/xx235300) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run public web research, search multiple engines, fetch public pages, and consolidate source metadata when an API-key-free workflow is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and target URLs may be sent to search engines or third-party fetch services. <br>
Mitigation: Use only public, non-sensitive queries and URLs; avoid confidential terms, internal or private-network URLs, credentials, and tokenized links. <br>
Risk: Dependency and browser-based fetching can vary by environment and dependency version. <br>
Mitigation: Run the skill in an isolated environment and pin dependencies for repeatable installs; install browser support only when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xx235300/smart-research) <br>
- [Declared project homepage](https://github.com/xx235300/smart-research) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON] <br>
**Output Format:** [Structured JSON/dict by default, with optional Markdown reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes titles, URLs, snippets or fetched content, source engine or fetch method, scores, timestamps, and error details when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
