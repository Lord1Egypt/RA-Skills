## Description: <br>
视频文件批量重命名和整理工具，支持按时间、格式、分辨率等方式整理视频，批量重命名，预览模式和撤销功能！ <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utopiabenben](https://clawhub.ai/user/utopiabenben) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to organize local video folders, copy videos into date or format folders, and batch-rename video files with preview and undo support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk organization and rename operations can affect important local video collections, and undo behavior should be checked before relying on it. <br>
Mitigation: Run preview mode first, test on a small folder, and keep a separate backup before using it on irreplaceable or sensitive media. <br>
Risk: Undo may depend on the generated backup file and may not match expectations if copied outputs or backup state change. <br>
Mitigation: Confirm how organize and undo behave in the target workflow before deleting originals or cleaning generated output folders. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/utopiabenben/video-organizer) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, text] <br>
**Output Format:** [Markdown or terminal text with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can guide local copy, rename, preview, and undo workflows for video files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version and SKILL.md changelog, released 2026-03-06) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
