## Description: <br>
Use TabTab to run AI-powered tasks through REST API helper scripts for task creation, file uploads, status polling, event logs, task termination, and sandbox output downloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bjwswang](https://clawhub.ai/user/bjwswang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to submit prompts and files to TabTab, monitor remote multi-agent task execution, inspect event logs, and retrieve generated outputs such as analysis results, research reports, charts, slide decks, and sandbox files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, uploaded files, database contents, event logs, and downloaded ZIP files may contain sensitive data because the skill sends user-directed work to TabTab. <br>
Mitigation: Verify TABTAB_BASE_URL, use a revocable API key where possible, avoid sending unnecessary sensitive data, and clean up local /tmp outputs that contain private data. <br>
Risk: TABTAB_API_KEY is required for every API call and could be exposed if stored or logged carelessly. <br>
Mitigation: Keep the key out of committed files and shared logs, prefer a secrets manager or protected environment variable, and rotate the key if exposure is suspected. <br>
Risk: Remote task outputs, event logs, and downloaded archives may include incorrect, incomplete, or unexpected generated content. <br>
Mitigation: Review task status, event logs, and downloaded results before using them in downstream work. <br>


## Reference(s): <br>
- [TabTab Skill release page](https://clawhub.ai/bjwswang/tabtab) <br>
- [TabTab API key settings](https://tabtabai.com/api-key) <br>
- [TabTab OpenPlatform base URL](https://tabtabai.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, text, markdown] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May upload user-selected files and download ZIP archives from remote TabTab task sandboxes.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
