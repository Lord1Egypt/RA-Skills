## Description: <br>
Generate videos using the Volcengine Doubao Seedance 2.0 model series. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fackee](https://clawhub.ai/user/fackee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to generate, edit, or extend short videos through Volcengine Doubao Seedance 2.0 using text prompts and optional image, video, or audio references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, public media URLs, and generation settings are sent to Volcengine's cloud API. <br>
Mitigation: Do not submit sensitive, private, unauthorized, or regulated media or prompts unless the user has approved that third-party processing. <br>
Risk: ARK_API_KEY is required for API access. <br>
Mitigation: Keep the key in environment configuration, avoid pasting it into prompts or logs, and rotate it if exposure is suspected. <br>
Risk: The skill asks the agent to install volcengine-python-sdk[ark], which can modify the active Python environment. <br>
Mitigation: Install dependencies in an isolated environment when possible and review dependency changes before running the script. <br>
Risk: Generated video URLs are temporary and are documented as valid for 24 hours. <br>
Mitigation: Download or transfer generated videos promptly after successful task completion. <br>


## Reference(s): <br>
- [Seedance 2.0 API Parameter Reference](references/api-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/fackee/skills/seedance2-gen-video) <br>
- [Volcengine Ark API endpoint](https://ark.cn-beijing.volces.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API Calls] <br>
**Output Format:** [Markdown guidance with inline bash commands and generated video URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ARK_API_KEY, Volcengine API access, and public or platform asset URLs; generated video URLs are valid for 24 hours.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
