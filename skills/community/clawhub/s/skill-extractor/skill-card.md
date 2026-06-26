## Description: <br>
Export any installed OpenClaw skill into a shareable ZIP: detects and stages external runtime files, generates STRUCTURE.md for LLM-guided install, and reads and packages local files only. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seph1709](https://clawhub.ai/user/seph1709) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to export an installed skill, include referenced local runtime files after review, and produce a shareable ZIP with installation structure documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can package broad local folders or sensitive files into a shareable ZIP. <br>
Mitigation: Review the full file list for secrets, credentials, session files, app-data folders, and large recursive directories before approving an export. <br>
Risk: External files are packaged with their real values. <br>
Mitigation: Remove or replace live credentials before sharing the ZIP and proceed only after explicit user confirmation. <br>
Risk: A failed export can leave a staging folder behind. <br>
Mitigation: Delete leftover staging folders after failed runs and verify no sensitive files remain staged. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/seph1709/skill-extractor) <br>
- [Publisher Profile](https://clawhub.ai/user/seph1709) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, configuration, guidance] <br>
**Output Format:** [Markdown guidance and generated files, including STRUCTURE.md and a ZIP archive] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local-only packaging workflow with explicit user confirmation before external files are zipped.] <br>

## Skill Version(s): <br>
1.8.1 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
