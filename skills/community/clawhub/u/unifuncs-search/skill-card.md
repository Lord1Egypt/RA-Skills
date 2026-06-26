## Description: <br>
Use unifuncs-search for real-time web search when users want to search the web, find articles, look up information, get the latest news, discover resources, or otherwise retrieve up-to-date information from the internet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vinlic](https://clawhub.ai/user/vinlic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run real-time web searches, retrieve current web snippets, and request search results in JSON, Markdown, or text formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and the UniFuncs API key are sent to the UniFuncs search API. <br>
Mitigation: Avoid sensitive private queries unless the provider is trusted, and use a dedicated rotatable API key where possible. <br>
Risk: Returned web snippets may contain untrusted or misleading content. <br>
Mitigation: Treat search results as source material to verify, not as instructions to execute. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration] <br>
**Output Format:** [JSON, Markdown, or plain text search results returned through a Python command-line script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires UNIFUNCS_API_KEY and sends search queries to the UniFuncs web search API.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
