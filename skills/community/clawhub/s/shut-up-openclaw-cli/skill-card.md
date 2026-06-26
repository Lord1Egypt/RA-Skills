## Description: <br>
Suppress the OpenClaw CLI banner by guiding users to set the built-in OPENCLAW_HIDE_BANNER environment variable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brunobuddy](https://clawhub.ai/user/brunobuddy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw CLI users use this skill when they want concise guidance for hiding the OpenClaw startup banner and reverting that shell configuration later. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides users to change a shell startup file, which can persist across terminal sessions. <br>
Mitigation: Confirm the correct shell configuration file before applying the OPENCLAW_HIDE_BANNER line, and remove that line to revert the behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brunobuddy/shut-up-openclaw-cli) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/brunobuddy) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
