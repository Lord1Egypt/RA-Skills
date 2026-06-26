## Description: <br>
Generate Veo videos from natural language prompts through a Wanjie model service workflow with background task handling and result reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liangshenghzj888-stack](https://clawhub.ai/user/liangshenghzj888-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to trigger video generation from chat prompts and receive generated video links through local result handling. It is suited to automated video creation workflows that can tolerate background execution and external model-service calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the OpenClaw API-key configuration and sends prompts with a bearer token to Wanjie's service. <br>
Mitigation: Use a Wanjie-specific, least-privilege credential where possible and review the external service before submitting sensitive prompts. <br>
Risk: Detached background execution and scheduled monitoring can continue work outside the visible chat interaction. <br>
Mitigation: Install only where background workers are acceptable, review the scheduled task behavior, and document how users can stop or disable monitoring. <br>
Risk: The skill can install Python dependencies at runtime. <br>
Mitigation: Prefer preinstalling and pinning dependencies from a reviewed environment before first use. <br>
Risk: Returned links may be opened automatically without domain validation. <br>
Mitigation: Validate result-link domains and ask for user confirmation before opening links. <br>


## Reference(s): <br>
- [Wanjie Ark Model Service Platform](https://www.wjark.com/) <br>
- [ClawHub release page](https://clawhub.ai/liangshenghzj888-stack/wanjie-openclaw-video-v1-0-0) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/liangshenghzj888-stack) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Plain text status replies, local text result files, and generated video links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs background Python workers, writes local log/result files, and may open returned links automatically.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
