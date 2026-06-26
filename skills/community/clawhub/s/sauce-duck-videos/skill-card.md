## Description: <br>
Generates multilingual humorous sauce duck meme videos by configuring and running a RunningHub video workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emwstudio](https://clawhub.ai/user/emwstudio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to configure a RunningHub host and API key, start a multilingual sauce duck meme video workflow, and receive the completed MP4 link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill saves and may expose a RunningHub API key through local OpenClaw configuration and command execution. <br>
Mitigation: Use a limited or disposable RunningHub key, avoid logged terminals or automation, and rotate the key if it may have been exposed. <br>
Risk: The skill changes global OpenClaw configuration for the RunningHub host and API key. <br>
Mitigation: Review the configured values before running tasks and verify the host is www.runninghub.cn or www.runninghub.ai. <br>
Risk: Video generation depends on an external RunningHub workflow and may fail or time out. <br>
Mitigation: Keep the task ID from the response and use the query flow to check status or diagnose failures later. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/emwstudio/sauce-duck-videos) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown text with JSON status outputs and a video URL when generation succeeds] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python, a RunningHub API key, and a configured RunningHub host.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
