## Description: <br>
Automates Weibo post image generation, browser-based publishing, scheduled content workflows, and temporary file cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apple-sugar-xing](https://clawhub.ai/user/apple-sugar-xing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and social media operators use this skill to generate Weibo card images and publish posts through a logged-in browser. It also provides content-type guidance and cron-based scheduling patterns for recurring posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish public posts from a logged-in Weibo account. <br>
Mitigation: Use a test account or separate browser profile and require manual review before each post is submitted. <br>
Risk: Scheduled cron workflows can post without timely human review. <br>
Mitigation: Avoid unattended cron jobs until a dry-run or explicit approval gate is added. <br>
Risk: Cleanup commands delete files matching broad patterns in user picture and temporary folders. <br>
Mitigation: Change cleanup to a dedicated temporary directory and delete only files created by the current run. <br>
Risk: Browser automation can take screenshots and overwrite clipboard contents during publishing. <br>
Mitigation: Run in a separate browser profile or desktop session and keep unrelated sensitive content out of the clipboard and visible browser windows. <br>


## Reference(s): <br>
- [Weibo Auto Post release page](https://clawhub.ai/apple-sugar-xing/weibo-auto-post) <br>
- [Weibo content types guide](references/content_types.md) <br>
- [Weibo cron scheduling guide](references/cron_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell and PowerShell command examples; generated PNG image files when scripts are run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May publish to a live Weibo account through desktop and browser automation when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
