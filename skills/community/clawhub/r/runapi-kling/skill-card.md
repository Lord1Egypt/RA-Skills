## Description: <br>
Generate and edit video with Kling through RunAPI, using the RunAPI CLI for one-off tasks and SDKs for application integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runapi-ai](https://clawhub.ai/user/runapi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create, edit, or transform videos with Kling through RunAPI. It is suited to one-off CLI-driven video tasks and SDK guidance for application integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, request JSON, and supplied media may be sent to RunAPI/Kling. <br>
Mitigation: Use the skill only for intended RunAPI/Kling generation tasks and avoid sending secrets or sensitive personal data unless that sharing is intentional and approved. <br>
Risk: The skill can use an existing RunAPI login or RUNAPI_API_KEY when available. <br>
Mitigation: Confirm the active RunAPI account, provider billing, and credential scope before running generation commands. <br>
Risk: The workflow depends on the external runapi binary installed from a Homebrew tap. <br>
Mitigation: Review the Homebrew tap and installed CLI source before deployment in managed environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/runapi-ai/runapi-kling) <br>
- [RunAPI Kling model overview](https://runapi.ai/models/kling.md) <br>
- [RunAPI Kuaishou provider comparison](https://runapi.ai/providers/kuaishou.md) <br>
- [RunAPI model catalog](https://runapi.ai/models.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, code, configuration] <br>
**Output Format:** [Markdown with shell commands and SDK package names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include request-file guidance for RunAPI CLI tasks.] <br>

## Skill Version(s): <br>
0.2.4 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
