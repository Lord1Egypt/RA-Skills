## Description: <br>
Yeelight Smart Home helps compatible agent hosts control, organize, diagnose, design, personalize, recommend, and answer product questions for a Yeelight smart home through the local yeelight-home Runtime. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yeelight](https://clawhub.ai/user/yeelight) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage Yeelight homes, rooms, devices, groups, scenes, automations, diagnostics, lighting design, recommendations, and product knowledge through a local runtime-backed agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help manage smart-home state and persistent configuration through a separately installed local runtime. <br>
Mitigation: Install it only when you trust the yeelight-home runtime and want an agent to manage the Yeelight home. <br>
Risk: Persistent, destructive, or account-impacting actions may change home configuration. <br>
Mitigation: Review pending plans carefully and use the runtime's local approval flow for high-impact actions before committing them. <br>
Risk: Credentials or tokens could be exposed if users paste them into chat. <br>
Mitigation: Authenticate through the local runtime or terminal flow and never paste tokens, passwords, cookies, or other secrets into chat. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yeelight/skills/yeelight-smart-home) <br>
- [Yeelight Publisher Profile](https://clawhub.ai/user/yeelight) <br>
- [README](README.md) <br>
- [Skill Contract](SKILL.md) <br>
- [Safety And Confirmation](references/safety-and-confirmation.md) <br>
- [Capability Boundaries](references/capability-boundaries.md) <br>
- [Runtime Status And Errors](references/runtime-status-and-errors.md) <br>
- [Runtime Manifest](scripts/runtime-manifest.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown responses with inline shell commands and structured runtime JSON requests or responses when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runtime actions use yeelight-home invoke --stdin; persistent or high-impact changes require runtime confirmation or local approval.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
