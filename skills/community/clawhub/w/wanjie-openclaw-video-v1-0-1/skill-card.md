## Description: <br>
Generates videos from natural-language prompts through the Wanjie Ark Veo model service for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liangshenghzj888-stack](https://clawhub.ai/user/liangshenghzj888-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users can trigger video generation from chat by sending a supported video prompt. The skill submits the request to Wanjie, monitors the background job, and returns or records the generated video link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the first API key from ~/.openclaw/openclaw.json and sends video prompts to Wanjie. <br>
Mitigation: Install only after confirming that the selected API key is the intended Wanjie key and that prompt content may be sent to that service. <br>
Risk: The skill can run detached background jobs and its documentation claims recurring monitoring without clear disable or uninstall steps. <br>
Mitigation: Review running processes and any scheduled task behavior after installation, and remove the skill if background execution is not acceptable. <br>
Risk: Returned links may be opened automatically in the local browser. <br>
Mitigation: Use in an environment where automatic browser opening is acceptable, or review and modify that behavior before running the skill. <br>
Risk: The skill writes logs, raw responses, and result links under its script directory. <br>
Mitigation: Inspect and clear those files when they may contain sensitive prompts, service responses, or generated media links. <br>
Risk: The helper interface may install the requests dependency automatically if it is missing. <br>
Mitigation: Prefer installing dependencies explicitly in a controlled Python environment before invoking the skill. <br>


## Reference(s): <br>
- [Wanjie Ark model service](https://www.wjark.com/) <br>
- [ClawHub release page](https://clawhub.ai/liangshenghzj888-stack/wanjie-openclaw-video-v1-0-1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, API Calls, Guidance] <br>
**Output Format:** [Plain text status messages plus local result and log files containing task status or a video URL.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs video generation asynchronously and may open the returned video URL in a browser.] <br>

## Skill Version(s): <br>
1.0.0 (source: manifest.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
