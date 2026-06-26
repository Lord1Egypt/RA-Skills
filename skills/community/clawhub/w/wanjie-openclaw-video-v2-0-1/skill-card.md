## Description: <br>
Generates Veo videos from natural-language prompts in OpenClaw using the Wanjie Ark model service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liangshenghzj888-stack](https://clawhub.ai/user/liangshenghzj888-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to submit a Chinese natural-language video prompt and receive a generated Veo video link through an automated background workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses credentials from the local OpenClaw configuration for video-generation API calls. <br>
Mitigation: Use a dedicated, limited API key and avoid sending private or secret material in prompts. <br>
Risk: Background execution and monitor behavior may continue work without direct user interaction. <br>
Mitigation: Review whether the OpenClaw_Veo_Monitor scheduled task or background monitor is created, and disable or remove it if unattended execution is not desired. <br>
Risk: Prompt and payload details may be written to local logs. <br>
Mitigation: Treat prompts as potentially logged data and review or clear local logs according to the deployment's data-handling policy. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/liangshenghzj888-stack/wanjie-openclaw-video-v2-0-1) <br>
- [Wanjie Ark model service platform](https://www.wjark.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Files] <br>
**Output Format:** [Plain text status messages plus a generated video link recorded in local result and log files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs background video-generation work and may open the generated URL automatically.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata; artifact manifest reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
