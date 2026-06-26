## Description: <br>
Automatically generate Veo videos from natural-language OpenClaw chat commands with background monitoring, dependency handling, and timeout recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liangshenghzj888-stack](https://clawhub.ai/user/liangshenghzj888-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to submit video-generation prompts from chat and have the skill call Wanjie's Veo model workflow in the background. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a local OpenClaw API key and sends prompts to Wanjie. <br>
Mitigation: Use a dedicated Wanjie key, avoid sensitive prompts, and review local credential access before enabling the skill. <br>
Risk: The skill starts detached background jobs and may leave worker or scheduled-task behavior running outside the chat session. <br>
Mitigation: Confirm how to stop or remove any running worker or scheduled task before use, and monitor local logs/results during initial runs. <br>
Risk: Generated prompts, results, and returned links are logged locally and returned links may open automatically. <br>
Mitigation: Review local log/result files and only use prompts and environments where automatic link opening is acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/liangshenghzj888-stack/wanjie-openclaw-video-v2-0) <br>
- [Wanjie Ark model service platform](https://www.wjark.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls, Files, Guidance] <br>
**Output Format:** [Markdown and chat text with generated video links recorded in local text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Starts detached background video-generation workers, reads an OpenClaw API key, writes local logs/results, and may open returned video links automatically.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
