## Description: <br>
RunAPI MCP Server helps agents generate images, video, music, audio, speech, and other media through RunAPI task submission and polling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runapi-ai](https://clawhub.ai/user/runapi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to turn media-generation requests into validated RunAPI tasks, track task status, and present generated output URLs and cost fields when available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests may be sent to RunAPI for external task processing. <br>
Mitigation: Confirm sensitive, ambiguous, or expensive media requests before submitting tasks. <br>
Risk: Some task creation can incur provider costs. <br>
Mitigation: Ask for confirmation before video, music, batch, or otherwise costly task creation. <br>
Risk: Generated output URLs may be temporary. <br>
Mitigation: Download and store generated files in durable storage before treating outputs as production assets. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Markdown] <br>
**Output Format:** [Markdown status updates with task identifiers, output URLs, cost fields when available, and follow-up guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated file URLs may be temporary; durable use requires downloading and storing generated files separately.] <br>

## Skill Version(s): <br>
0.1.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
