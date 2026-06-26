## Description: <br>
Deploy static websites to Static.app hosting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Akellacom](https://clawhub.ai/user/Akellacom) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to deploy, update, inspect, download, and delete static sites hosted on Static.app from an OpenClaw workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can manage Static.app resources using the user's API key, including upload, download, inspection, and deletion. <br>
Mitigation: Use the least-privileged Static.app API key available and install the skill only when OpenClaw should manage the Static.app account. <br>
Risk: Deleting a site or updating the wrong project PID can remove or change hosted content. <br>
Mitigation: Verify the PID before running update or delete commands, and avoid --force unless deletion is explicitly intended. <br>
Risk: Downloaded archives can overwrite files in the selected output path during extraction. <br>
Mitigation: Download only from trusted sites and choose an output directory where overwrites are acceptable. <br>


## Reference(s): <br>
- [Static.app](https://static.app) <br>
- [Static.app API keys](https://static.app/account/api) <br>
- [ClawHub skill page](https://clawhub.ai/Akellacom/static-app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Static.app site URLs, project PIDs, file listings, downloaded site files, and raw JSON responses when requested.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
