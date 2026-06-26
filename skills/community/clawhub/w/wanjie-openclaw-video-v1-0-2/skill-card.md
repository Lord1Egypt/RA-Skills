## Description: <br>
Generates Veo videos from natural-language prompts on OpenClaw using Wanjie's model API, with background processing, timeout handling, and result logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liangshenghzj888-stack](https://clawhub.ai/user/liangshenghzj888-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to submit Chinese natural-language video prompts, run Veo generation in the background, and retrieve generated video result links through local result files and browser opening. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read an API key from the global OpenClaw configuration and send prompts to Wanjie's remote API. <br>
Mitigation: Use a skill-scoped API key where possible, limit the key's privileges, and avoid submitting confidential prompts unless the remote service is approved for that data. <br>
Risk: The skill starts detached Python background processes and may create scheduled or recurring monitoring behavior. <br>
Mitigation: Review active background processes and scheduled tasks after installation, and remove the OpenClaw_Veo_Monitor task or related process if the skill is no longer needed. <br>
Risk: The skill may install Python dependencies at runtime. <br>
Mitigation: Install and pin dependencies in a controlled environment before use, or review runtime package installation activity before allowing execution. <br>
Risk: The skill writes local log and result files and can automatically open generated remote links. <br>
Mitigation: Inspect generated URLs before reuse, review local log/result files for sensitive content, and run the skill in an environment where automatic browser opening is acceptable. <br>


## Reference(s): <br>
- [Wanjie Ark Model Service Platform](https://www.wjark.com/) <br>
- [ClawHub release page](https://clawhub.ai/liangshenghzj888-stack/wanjie-openclaw-video-v1-0-2) <br>
- [Publisher profile](https://clawhub.ai/user/liangshenghzj888-stack) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, shell commands, configuration, guidance] <br>
**Output Format:** [Text responses, local log/result files, and generated video URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Starts detached Python background work, reads an OpenClaw API key, writes veo_log.txt, last_response.txt, and veo_result.txt, and may open generated result links in a browser.] <br>

## Skill Version(s): <br>
1.0.0 (source: manifest.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
