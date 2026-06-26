## Description: <br>
Feishu Bitable Storage Manager - Integrated tool for item storage, retrieval, and location updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruoruochen](https://clawhub.ai/user/ruoruochen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage personal item locations in Feishu Bitable, including adding stored items, searching for where items are kept, and updating item locations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled test code contains real-looking Feishu credentials. <br>
Mitigation: Do not run the bundled test as-is; remove the credentials before use and rotate them if they were real. <br>
Risk: The skill can upload item names, locations, and optional images to Feishu Bitable. <br>
Mitigation: Use a dedicated Feishu app with minimal Bitable and file-upload permissions, and upload only data intended to be stored in Feishu. <br>
Risk: The install script changes local executable permissions, may install the requests package, and can create a storage-manager symlink. <br>
Mitigation: Review install.sh before execution and install in an environment where those local changes are expected. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ruoruochen/release-package) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls] <br>
**Output Format:** [Command-line text output with configuration guidance and Feishu Bitable API actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3, the requests library, Feishu app credentials, a Bitable token, and a table ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
