## Description: <br>
Searches the web with Volcengine and returns up to five summary results for a clear query. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[warm-wm](https://clawhub.ai/user/warm-wm) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and agents use this skill to run targeted public web searches through Volcengine and summarize the returned search results without adding unsupported content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to Volcengine. <br>
Mitigation: Avoid putting secrets, private data, or sensitive internal details into search queries. <br>
Risk: The skill uses Volcengine credentials or VeFaaS IAM credentials to call the search API. <br>
Mitigation: Use least-privilege, tool-scoped credentials and review credential access before deployment. <br>
Risk: The skill depends on the veadk package for authentication, logging, and request signing. <br>
Mitigation: Verify the veadk dependency source and version before use. <br>


## Reference(s): <br>
- [Volcengine Web Search Documentation](https://www.volcengine.com/docs/85508/1650263) <br>
- [ClawHub skill page](https://clawhub.ai/warm-wm/volcengine-web-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Console text output containing a Python list of summary strings, with guidance usually delivered as Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns up to 5 summary items from the Volcengine web search response.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
