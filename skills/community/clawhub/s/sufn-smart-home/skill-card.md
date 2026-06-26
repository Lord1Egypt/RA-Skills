## Description: <br>
三峰智能 controls SUFN smart-home accounts by logging in, syncing homes, listing devices and scenes, and issuing real API calls for device control and scene execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lingguyuan](https://clawhub.ai/user/lingguyuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to operate SUFN smart-home devices and scenes through an agent, including account login, household switching, device synchronization, device listing, scene listing, device control, and scene execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store a reusable home-control token in state.json. <br>
Mitigation: Use only in a trusted local workspace, limit access to the saved state file, and clear the saved state or revoke the session when the skill is no longer needed. <br>
Risk: Ambiguous scene or mode phrases can trigger broad real-world device changes. <br>
Mitigation: Prefer exact device or scene names, review matched scenes before high-impact actions, and avoid vague commands when multiple devices or scenes could match. <br>
Risk: The server security verdict is suspicious because the skill controls real smart-home devices through live API calls. <br>
Mitigation: Review before installing, test with low-impact commands first, and monitor returned API results rather than assuming an action succeeded. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lingguyuan/sufn-smart-home) <br>
- [SUFN Open API Base URL](https://open.aibasis.cc) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown with PowerShell, bash, JSON, and concise status responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces state JSON for local persistence and concise success or failure messages based on live API responses.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
