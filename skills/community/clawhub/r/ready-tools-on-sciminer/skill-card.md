## Description: <br>
Discover a user-specified SciMiner tool from the published API-doc index, read its Markdown description, and invoke it through the SciMiner internal API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sciminer](https://clawhub.ai/user/sciminer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to discover a named SciMiner tool, inspect its current API documentation, submit requests with the required parameters or uploaded files, and return a shareable result link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a SciMiner API key and authorizes API calls with sensitive credentials. <br>
Mitigation: Use a dedicated SciMiner API key for this workflow, store it only at the documented credential path, and ensure responses or logs do not expose the key. <br>
Risk: The skill may upload local files to SciMiner when selected tool documentation requires file inputs. <br>
Mitigation: Review file contents before upload and avoid submitting sensitive or proprietary files unless sharing them with SciMiner is intended. <br>
Risk: The skill relies on live remote tool documentation to determine request schemas and endpoints. <br>
Mitigation: Verify that selected documentation and generated calls target the expected SciMiner domain before sending credentials, files, or requests. <br>


## Reference(s): <br>
- [SciMiner tool API documentation index](https://sciminer.tech/tool_api_files/) <br>
- [SciMiner API key utility](https://sciminer.tech/utility) <br>
- [ClawHub skill page](https://clawhub.ai/sciminer/ready-tools-on-sciminer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with inline code, JSON result summaries, and shareable SciMiner URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated invocation code, task status, task_id, and share_url; API keys must not be exposed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
