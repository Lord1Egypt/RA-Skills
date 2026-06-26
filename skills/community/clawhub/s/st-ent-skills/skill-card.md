## Description: <br>
Searches 699pic enterprise photo and video assets, checks whether assets were downloaded, inspects download records, and generates download links through a local 699pic OpenAPI integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[st699pic](https://clawhub.ai/user/st699pic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and enterprise users with authorized 699pic access use this skill to search photo and video assets, review download status and history, and generate download links through a local MCP or direct OpenAPI workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated network access can send business search terms or account-related data to the 699pic service. <br>
Mitigation: Use the skill only for explicit 699pic requests, review requests before execution, and configure a least-privilege SERVICE_API_KEY where available. <br>
Risk: Broad media-search triggers may activate the skill for generic image or video requests. <br>
Mitigation: Tighten activation to explicit 699pic enterprise workflows before deployment. <br>
Risk: Local MCP registration or service endpoint configuration may differ across machines. <br>
Mitigation: Inspect the local mcporter configuration, command, environment variables, permissions, and SERVICE_API_BASE_URL before use. <br>


## Reference(s): <br>
- [699pic OpenAPI MCP Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/st699pic/st-ent-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API Calls, Configuration instructions, JSON] <br>
**Output Format:** [Markdown summaries with embedded image previews, shell command examples, and optional JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an authorized SERVICE_API_KEY and may use SERVICE_API_BASE_URL, node, and mcporter depending on the selected route.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
