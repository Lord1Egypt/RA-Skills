## Description: <br>
WPS Office automation skill supporting document creation, Markdown conversion, and image-text layout. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lilei0311](https://clawhub.ai/user/lilei0311) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and office automation users use this skill to create, open, convert, and batch-process WPS Office documents, including Markdown-to-Word, Excel, and PPT workflows. It also supports image insertion and image-text layouts for Word, Excel, and PPT outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify local documents and batch-process folders. <br>
Mitigation: Run it only on trusted files, keep backups for important folders, and review target paths before batch operations. <br>
Risk: Desktop automation can interact with the active WPS window. <br>
Mitigation: Keep the intended WPS window focused and test workflows in a controlled environment before using them on important documents. <br>
Risk: Optional WPS 365 features use app credentials stored in local configuration. <br>
Mitigation: Leave WPS 365 credentials blank unless cloud features are needed and protect or rotate credentials if configured. <br>


## Reference(s): <br>
- [ClawHub Wps Skill listing](https://clawhub.ai/lilei0311/wps-skill) <br>
- [WPS Open Platform](https://open.wps.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Markdown, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated Office or Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, open, modify, or convert local WPS Office documents and can optionally use WPS 365 credentials for cloud features.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
