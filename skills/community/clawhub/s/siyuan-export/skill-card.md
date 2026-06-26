## Description: <br>
Exports SiYuan notes to Word (.docx) files through a local SiYuan API, supporting document ID, path, and title search workflows for single-document and child-document batch exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chimyves](https://clawhub.ai/user/chimyves) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and SiYuan users use this skill to export local SiYuan documents and nested child documents into portable Word files, with structured JSON responses for agent parsing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill needs access to a local SiYuan instance and its API token. <br>
Mitigation: Keep the SiYuan token private, prefer environment variables or a protected config.json, and verify the baseURL points to the intended trusted SiYuan server. <br>
Risk: Exports may write sensitive notes to user-selected Word files and output directories. <br>
Mitigation: Choose output folders carefully and review exported documents before sharing or moving them outside the local environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chimyves/siyuan-export) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Shell commands, Configuration] <br>
**Output Format:** [JSON status responses and exported .docx files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local SiYuan API configuration from environment variables or config files.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
