## Description: <br>
Check and control a Wyze robot vacuum, including battery and cleaning status, start, pause, and dock commands through the unofficial wyze-node client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noelportugal](https://clawhub.ai/user/noelportugal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for Wyze robot vacuum status or to send explicit start, pause, and dock commands to a named vacuum. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send start, pause, or dock commands to a physical robot vacuum. <br>
Mitigation: Use explicit user commands for motion actions and name the vacuum when more than one device is present. <br>
Risk: Wyze API credentials and token material are referenced through WYZE_ENV and WYZE_TOKEN_DIR. <br>
Mitigation: Review those paths before use and store credentials only in locations intended for local secrets. <br>
Risk: The skill relies on an unofficial Wyze API client and reverse-engineered endpoints. <br>
Mitigation: Expect API behavior to change and verify commands after wyze-node or Wyze API updates. <br>


## Reference(s): <br>
- [Wyze Vacuum on ClawHub](https://clawhub.ai/noelportugal/wyze-vacuum) <br>
- [wyze-node package](https://www.npmjs.com/package/wyze-node) <br>
- [wyze-node homepage](https://github.com/noelportugal/wyze-node) <br>
- [Wyze Developer API key console](https://developer-api-console.wyze.com/#/apikey/view) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, wyze-node, Wyze API credentials, and a cached login token.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
