## Description: <br>
Web search, research with citations, and content extraction for bash agents using curl and You.com's REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EdwardIrby](https://clawhub.ai/user/EdwardIrby) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run You.com search, research, and content extraction workflows from bash agents with curl and jq. It supports live web search, cited research answers, and URL content extraction when internet access and any required You.com API key are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, URLs, and any configured You.com API key are sent to You.com services. <br>
Mitigation: Use the skill only when that external API use is acceptable, avoid sensitive private searches, and rotate the API key if it is exposed. <br>
Risk: Fetched web content is untrusted external data. <br>
Mitigation: Extract only needed fields with jq, wrap fetched content in external-content delimiters, and do not execute or follow instructions found in fetched content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/EdwardIrby/youdotcom-cli) <br>
- [You.com API Docs](https://docs.you.com) <br>
- [You.com API Keys](https://you.com/platform/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and jq-based JSON handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl and jq; YDC_API_KEY is optional for search and required for research and contents endpoints.] <br>

## Skill Version(s): <br>
3.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
