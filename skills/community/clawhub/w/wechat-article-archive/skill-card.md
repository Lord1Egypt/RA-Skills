## Description: <br>
Save WeChat Official Account articles from mp.weixin.qq.com links into a user-specified local folder as Markdown plus a local assets image folder. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harven-droid](https://clawhub.ai/user/harven-droid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users who need local archives of WeChat Official Account articles use this skill to save a provided article URL into a specified folder as Markdown with downloaded image assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports that the parser can execute code from fetched pages. <br>
Mitigation: Review before installing, use only trusted WeChat article links, and run the skill in a constrained sandbox. <br>
Risk: The security scan reports that URL checks can be bypassed. <br>
Mitigation: Treat the skill as review-required until the publisher replaces substring URL checks with strict parsed-host validation. <br>
Risk: The skill writes Markdown and image files to a local destination folder. <br>
Mitigation: Choose a dedicated output folder and review the generated paths and JSON result before relying on the archive. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/harven-droid/skills/wechat-article-archive) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown file, local assets folder, and JSON verification output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes to a user-specified local folder; image downloads can be skipped or bounded with a timeout.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
