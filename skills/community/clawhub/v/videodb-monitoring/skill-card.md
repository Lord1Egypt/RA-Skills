## Description: <br>
Screen recording capabilities. Generate stream URLs, search recordings, get transcripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omgate234](https://clawhub.ai/user/omgate234) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to record task execution, generate playable VideoDB stream URLs, and query indexed screen or audio activity for summaries, search results, and transcripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent screen and possible system-audio monitoring can capture sensitive activity. <br>
Mitigation: Install and run only when that monitoring is intentional, confirm capture status before use, and stop the monitor when recording is no longer needed. <br>
Risk: Indexed recordings, summaries, and transcripts may expose private data. <br>
Mitigation: Start indexing only for requested search, summary, or transcript tasks, stop indexing afterward, and delete recordings or transcripts according to VideoDB controls when retention is not needed. <br>
Risk: Generated recording or player URLs may disclose captured private content if shared broadly. <br>
Mitigation: Share stream and player URLs only with intended recipients and avoid generating share links for sensitive time ranges. <br>
Risk: VideoDB API keys are required for operation and could be exposed if mishandled. <br>
Mitigation: Store API keys in OpenClaw configuration or environment variables, do not paste them into shared outputs, and rotate them if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/omgate234/videodb-monitoring) <br>
- [Publisher profile](https://clawhub.ai/user/omgate234) <br>
- [VideoDB console](https://console.videodb.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with shell commands, stream URLs, summaries, search results, and transcripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VIDEODB_API_KEY and a VideoDB capture session; indexing is started explicitly for search, summaries, and transcripts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
