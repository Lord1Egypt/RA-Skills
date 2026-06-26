## Description: <br>
Exports all documents in a selected Yuque knowledge base to local Markdown while preserving the directory structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sh1-5](https://clawhub.ai/user/sh1-5) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge-work users use this skill to export Yuque repositories they are authorized to access into local Markdown files, with optional local copies of embedded images. It is intended for browser-session based migration, backup, and offline editing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an authenticated browser session to access Yuque content, so exported documents may contain sensitive workspace information. <br>
Mitigation: Use it only for Yuque repositories you are authorized to copy, and prefer a dedicated browser profile or account for sensitive workspaces. <br>
Risk: A broad or unintended output path can save many Markdown files and optional images to an unexpected location. <br>
Mitigation: Verify the target Yuque URL and choose a specific output folder before running the export. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sh1-5/yuque-export) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/sh1-5) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Code, Guidance, Files] <br>
**Output Format:** [Markdown files plus progress and completion guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves Yuque folder hierarchy, can place downloaded images under _assets, and reports export counts and failures.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
