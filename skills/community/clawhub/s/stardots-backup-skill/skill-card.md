## Description: <br>
Automatically uploads selected local image files to Stardots.io cloud storage, lists stored files, and returns access links using configured API credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keepchen](https://clawhub.ai/user/keepchen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to back up explicitly selected image files to a configured Stardots.io space and retrieve uploaded file links or file listings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images are sent to Stardots.io, which can expose sensitive content depending on Stardots.io retention and link-sharing behavior. <br>
Mitigation: Upload only intended non-sensitive images unless Stardots.io retention, access, and sharing controls have been reviewed. <br>
Risk: Broad or generic file requests can lead the agent to list or upload unintended files. <br>
Mitigation: Prefer explicit commands with specific image paths or list requests for the configured Stardots.io space. <br>
Risk: The skill depends on Stardots.io API credentials for authenticated uploads and file listing. <br>
Mitigation: Store API credentials only in the platform's secure configuration and rotate them if access is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/keepchen/stardots-backup-skill) <br>
- [Stardots.io](https://stardots.io) <br>
- [Stardots.io API documentation](https://stardots.io/en/documentation/openapi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-like text responses with upload status, URLs, help text, and file-list entries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include uploaded file URL, filename, file size, target space, or file-list data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
