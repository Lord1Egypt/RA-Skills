## Description: <br>
Generate AI videos, images, voice, and AI app outputs from the terminal using the Zyka CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[varshneyhars](https://clawhub.ai/user/varshneyhars) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to invoke Zyka CLI commands for media generation, editing, text-to-speech, talking-head video, and related AI media apps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected media may be sent to Zyka and downstream model providers. <br>
Mitigation: Avoid confidential, regulated, proprietary, or third-party identity media unless rights and consent are clear. <br>
Risk: The skill requires a Zyka API key and may spend paid credits when commands are executed. <br>
Mitigation: Protect and rotate ZYKA_API_KEY, use least-privilege access where available, and monitor Zyka dashboard usage. <br>


## Reference(s): <br>
- [Zyka AI skill page](https://clawhub.ai/varshneyhars/zyka-ai) <br>
- [Zyka homepage](https://zyka.ai) <br>
- [Zyka CLI package](https://www.npmjs.com/package/zyka) <br>
- [Zyka API keys](https://zyka.ai/settings/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce downloaded media files when the generated Zyka CLI commands are executed.] <br>

## Skill Version(s): <br>
0.4.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
