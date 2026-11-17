## Description:

Automatically generates Veo videos from natural-language commands with background monitoring, dependency handling, and timeout recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liangshenghzj888-stack](https://clawhub.ai/user/liangshenghzj888-stack)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to submit natural-language video prompts that trigger Wanjie/WJ Ark Veo video generation and return the resulting video link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads a local OpenClaw API key and sends requests to wanjiedata.com.

Mitigation: Use a dedicated Wanjie/OpenClaw API key with limited blast radius and rotate or revoke it if the environment is shared or compromised.

Risk: Video prompts are sent to an external video-generation service.

Mitigation: Avoid sensitive, confidential, personal, or regulated content in prompts unless the service terms and data handling are approved for that content.

Risk: The skill launches background Python processes and writes local logs and result files.

Mitigation: Run it in a controlled workspace, inspect local log/result files, and monitor or terminate background processes when generation is no longer needed.

Risk: The skill can install Python dependencies automatically.

Mitigation: Preinstall and pin approved dependencies in the runtime environment, or review dependency installation behavior before enabling the skill.

Risk: The skill automatically opens returned video links in a browser.

Mitigation: Use it only where automatic browser opening is acceptable, and review returned URLs before interacting with downloaded or hosted content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liangshenghzj888-stack/skills/wanjie-openclaw-video-v2-0)
- [Wanjie Ark model service platform](https://www.wjark.com/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text status messages, local result/log files, and returned video URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a background Python worker, local lock/result/log files, and browser opening for returned links.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
