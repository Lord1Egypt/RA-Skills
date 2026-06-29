## Description: <br>
Check and control a Wyze smart lock, including status, battery level, lock, and unlock, through the unofficial wyze-node API client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noelportugal](https://clawhub.ai/user/noelportugal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and home automation operators use this skill to check a Wyze lock's state and battery level, then lock or unlock a single named lock when the request is clear. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unlock commands can open a physical door. <br>
Mitigation: Confirm the exact lock name with the user before unlocking, act only on a single named lock, and refuse vague or ambiguous unlock requests. <br>
Risk: The skill uses an unofficial Wyze API integration with access to the user's Wyze account. <br>
Mitigation: Install only when the publisher and dependency chain are trusted, keep Wyze API credentials in the configured secrets file, and avoid running unlock actions from shared or untrusted chat surfaces. <br>
Risk: Wyze may change reverse-engineered endpoints used by wyze-node. <br>
Mitigation: Monitor failures, keep wyze-node updated, and revalidate lock, unlock, and status behavior after dependency or API changes. <br>


## Reference(s): <br>
- [ClawHub Wyze Lock release page](https://clawhub.ai/noelportugal/wyze-lock) <br>
- [wyze-node GitHub repository](https://github.com/noelportugal/wyze-node) <br>
- [wyze-node npm package](https://www.npmjs.com/package/wyze-node) <br>
- [Wyze Developer API key console](https://developer-api-console.wyze.com/#/apikey/view) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text status or action confirmation, with setup and safety guidance in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, wyze-node, Wyze API credentials, and a cached login token.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
