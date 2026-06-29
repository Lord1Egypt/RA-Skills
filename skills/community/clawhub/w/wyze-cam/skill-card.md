## Description: <br>
View and control Wyze cameras through a bundled Node.js CLI that wraps the unofficial wyze-node client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noelportugal](https://clawhub.ai/user/noelportugal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let an agent list Wyze cameras, retrieve cached thumbnails or live snapshots, and control named camera features such as siren, lights, motion detection, notifications, recording, and power. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Camera controls can affect the physical environment, especially sirens, floodlights, power state, recording, and garage-door-associated cameras. <br>
Mitigation: Require an explicit named-camera request before acting, confirm before enabling sirens or operating garage-related devices, and avoid applying actions to all cameras at once. <br>
Risk: The skill relies on Wyze account API credentials and cached login tokens. <br>
Mitigation: Keep WYZE_ENV and token directories private, preserve authenticated CLI checks, and limit use to agents trusted with the relevant Wyze account. <br>
Risk: The underlying Wyze access is unofficial and uses reverse-engineered endpoints that may change without notice. <br>
Mitigation: Verify behavior on the intended camera models, prefer cached thumbnails when a current frame is not required, and test live snapshots after dependency or API changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/noelportugal/wyze-cam) <br>
- [wyze-node package](https://www.npmjs.com/package/wyze-node) <br>
- [wyze-node project homepage](https://github.com/noelportugal/wyze-node) <br>
- [Wyze API key console](https://developer-api-console.wyze.com/#/apikey/view) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce camera thumbnail URLs or local JPG snapshot paths for the agent to attach to the user.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
