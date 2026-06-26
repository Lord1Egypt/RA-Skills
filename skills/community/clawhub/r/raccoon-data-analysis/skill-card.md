## Description: <br>
Helps agents use the Raccoon remote data-analysis API for session management, file upload and download, data visualization, and interactive analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raccoon-office](https://clawhub.ai/user/raccoon-office) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data analysts use this skill to route requested analysis tasks to a configured Raccoon service, upload user-approved files, stream analysis responses, and retrieve generated artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads user-selected files to the configured Raccoon API host for remote analysis. <br>
Mitigation: Use it only with files the user is allowed to send, confirm the configured host is trusted and uses HTTPS, and avoid uploading sensitive or confidential data unless approved. <br>
Risk: Provider-controlled result files may be saved locally and opened too broadly. <br>
Mitigation: Review downloaded artifact filenames and contents before opening them, and prefer non-automatic opening until filenames are sanitized and opening is explicitly requested. <br>
Risk: One authentication-check workflow may expose part of the API token in captured logs. <br>
Mitigation: Avoid running token checks in shared or logged terminals, and rotate the token if it may have been exposed. <br>


## Reference(s): <br>
- [Raccoon Data Analysis on ClawHub](https://clawhub.ai/raccoon-office/raccoon-data-analysis) <br>
- [Raccoon website](https://xiaohuanxiong.com) <br>
- [API Reference](references/API_REFERENCE.md) <br>
- [API Cheatsheet](references/CHEATSHEET.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, local artifact paths, and streamed analysis summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 plus RACCOON_API_HOST and RACCOON_API_TOKEN environment variables; generated artifacts are saved under ./raccoon/dataanalysis/.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
