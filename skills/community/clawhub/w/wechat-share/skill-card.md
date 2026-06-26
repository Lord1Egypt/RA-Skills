## Description: <br>
Export and import selected OpenClaw workspace files between workspaces with optional burn-after-read. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuhao6741](https://clawhub.ai/user/liuhao6741) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to share selected workspace text files, preview received shares, and import validated files into another workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected workspace files are uploaded to a temporary external share. <br>
Mitigation: Review the final export list before upload and share only files intended for transfer. <br>
Risk: The db_id and api_token grant access to the shared files. <br>
Mitigation: Treat the share credentials as sensitive and use burn-after-read when appropriate. <br>
Risk: Imported files may overwrite existing workspace files or introduce untrusted agent/config content. <br>
Mitigation: Run preview first, review overwrite warnings and paths, and import agent or configuration files only from trusted sources. <br>
Risk: Workspace files may contain secrets or personal context. <br>
Mitigation: Avoid sharing secrets unless explicitly intended and confirmed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liuhao6741/wechat-share) <br>
- [Publisher Profile](https://clawhub.ai/user/liuhao6741) <br>
- [db9 Anonymous Registration API](https://api.db9.ai/customer/anonymous-register) <br>
- [db9 Databases API](https://api.db9.ai/customer/databases) <br>
- [examples.md](examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and compact recipient-facing instruction blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include share previews, import summaries, file lists, overwrite warnings, burn-after-read status, and sensitive token handling notes.] <br>

## Skill Version(s): <br>
1.0.8 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
