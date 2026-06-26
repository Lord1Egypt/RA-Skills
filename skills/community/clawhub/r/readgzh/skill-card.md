## Description: <br>
ReadGZH lets AI agents retrieve WeChat Official Account articles through a cloud API and return clean Markdown, cached article data, search results, or structured summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sweesama](https://clawhub.ai/user/sweesama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to let an AI assistant read, summarize, search, and reuse public WeChat Official Account article content without manually copying article HTML. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted WeChat article links, request metadata, and any ReadGZH API key are sent to ReadGZH's cloud service. <br>
Mitigation: Use only non-sensitive links and personal API keys; do not submit private, tokenized, internal, regulated, or sensitive URLs. <br>
Risk: Converted article content may be permanently cached and visible to other users. <br>
Mitigation: Treat submitted content as public and cacheable, and avoid content whose shared cached visibility would be unacceptable. <br>


## Reference(s): <br>
- [ReadGZH ClawHub listing](https://clawhub.ai/sweesama/readgzh) <br>
- [ReadGZH API documentation](https://readgzh.site/docs) <br>
- [ReadGZH dashboard and API key](https://readgzh.site/dashboard) <br>
- [ReadGZH support site](https://readgzh.site) <br>
- [Artifact OpenAPI specification](artifact/openapi.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, and configuration snippets with optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include paginated article chunks, cached article metadata, search results, summaries, and credit or rate-limit errors.] <br>

## Skill Version(s): <br>
1.6.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
