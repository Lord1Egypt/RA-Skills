## Description: <br>
Manage Roblox game passes and developer products via Open Cloud API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TeddyEngel](https://clawhub.ai/user/TeddyEngel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to manage Roblox experiences through the Open Cloud API, including listing games and creating, updating, listing, or retrieving game passes and developer products. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review automation may run nested review commands with broad local authority. <br>
Mitigation: Review the skill before installation and run review workflows without sandbox bypass unless elevated local authority is explicitly required. <br>
Risk: Commands can create or update monetized Roblox game passes and developer products through the user's API key. <br>
Mitigation: Use a scoped Roblox Open Cloud API key, restrict it to the required experiences and permissions, and review command arguments before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/TeddyEngel/roblox-cli) <br>
- [Roblox Open Cloud API Documentation](https://create.roblox.com/docs/cloud) <br>
- [Game Passes API](https://create.roblox.com/docs/cloud/reference/features/game-passes) <br>
- [Developer Products API](https://create.roblox.com/docs/cloud/reference/features/developer-products) <br>
- [API Keys Guide](https://create.roblox.com/docs/cloud/auth/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ROBLOX_API_KEY with appropriate Roblox Open Cloud permissions.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
