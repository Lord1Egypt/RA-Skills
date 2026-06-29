## Description: <br>
Automates batch uploading and management of Xianyu shop products on the Yidian backend using Playwright/CDP, with stepwise confirmation, screenshot-oriented validation, and optional Feishu status synchronization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuhao1443796193-commits](https://clawhub.ai/user/yuhao1443796193-commits) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers and operators who manage Xianyu shops through Yidian/ekadmin use this skill to parse product queues, publish listings, configure delivery options, and optionally sync completion status with Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish real shop listings and update Feishu records through an existing logged-in browser session. <br>
Mitigation: Use dry-run first, verify the logged-in Edge account and target shop before each run, and avoid production accounts until confirmation and rollback controls are in place. <br>
Risk: Hardcoded Feishu identifiers can point automation at a specific spreadsheet or workspace. <br>
Mitigation: Remove hardcoded Feishu identifiers and supply spreadsheet tokens through user-reviewed configuration or environment variables. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuhao1443796193-commits/skills/yidian-upload) <br>
- [README](artifact/README.md) <br>
- [CHANGELOG](artifact/CHANGELOG.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown guidance with Python and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can drive browser automation that publishes listings and updates Feishu records when connected to authenticated accounts.] <br>

## Skill Version(s): <br>
3.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
