## Description: <br>
Uses a Qwen-compatible vision API to describe local images and generate content-based filenames, with batch rename plans, apply mode, and rollback support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huiya-code](https://clawhub.ai/user/huiya-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect local image folders, create content-based Chinese filename plans, apply batch renames, and roll back applied renames when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected local images may be sent to the configured DashScope or Qwen-compatible vision endpoint. <br>
Mitigation: Use the skill only for images that are acceptable to share with that endpoint, and avoid public media URL mode unless the serving location and cleanup process are understood. <br>
Risk: Batch rename mode can modify filenames in an explicit or auto-selected image folder. <br>
Mitigation: Use an explicit folder, run a dry-run first, review the generated plan file, keep backups for important images, and retain the rollback file after applying changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huiya-code/qwen-vision-rename) <br>
- [DashScope OpenAI-compatible endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance plus JSON plan and rollback files from the CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write rename plan JSON files, rollback JSON files, and renamed local image files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
