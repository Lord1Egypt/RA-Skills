## Description: <br>
Use when managing QJZD Nav backups, restore, and site settings including uploading background images, logos, and favicons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nqdy666](https://clawhub.ai/user/nqdy666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to manage QJZD Nav backups, restore data, inspect or update settings, and upload background, logo, or favicon assets through the qjzd-nav CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backup deletion, backup import, settings updates, and asset uploads can change or delete QJZD Nav site data. <br>
Mitigation: Confirm the target site and exact filename, file path, or setting before running data-changing commands; inspect current state with list, get, or JSON output first. <br>
Risk: Importing the wrong backup data or uploading an unintended local asset can overwrite expected site state or public branding. <br>
Mitigation: Keep a current exported backup and verify supported file type, source path, and intended destination before import or upload. <br>


## Reference(s): <br>
- [Qjzd Nav Cli Operations on ClawHub](https://clawhub.ai/nqdy666/qjzd-nav-cli-operations) <br>
- [qjzd-nav CLI](../qjzd-nav-cli) <br>
- [qjzd-nav CLI Auth](../qjzd-nav-cli-auth) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include qjzd-nav commands that read, export, import, delete, update, or upload site data.] <br>

## Skill Version(s): <br>
1.3.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
