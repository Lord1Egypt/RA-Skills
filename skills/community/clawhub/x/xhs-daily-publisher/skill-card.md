## Description: <br>
Xhs Auto Publisher helps an agent configure, generate, render, and stage daily Xiaohongshu image posts while leaving the final publish action to the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gd269438407](https://clawhub.ai/user/gd269438407) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, social media operators, and developers use this skill to create a repeatable Xiaohongshu daily posting workflow, including topic selection, 9-image post copy, slide rendering, browser staging, and scheduling guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow stores Xiaohongshu login cookies and a persistent browser profile locally. <br>
Mitigation: Keep the .auth directory private, exclude it from git and synced folders, and delete saved cookies or profile data when access is no longer needed. <br>
Risk: The publishing helper opens an authenticated browser and uses automation settings that may affect account or platform policy risk. <br>
Mitigation: Review the browser automation before use, keep the manual final publish step, and remove clipboard permissions or anti-detection settings if they are not acceptable for the environment. <br>
Risk: Scheduled recurring runs can prepare posts repeatedly using current account context. <br>
Mitigation: Review every prepared post before publishing and disable or adjust the schedule when the account, topic, or compliance requirements change. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/gd269438407/xhs-daily-publisher) <br>
- [Xiaohongshu Creator Center](https://creator.xiaohongshu.com) <br>
- [Xiaohongshu](https://www.xiaohongshu.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with generated project files, HTML slide templates, JPEG image outputs, and Node.js/Puppeteer command steps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stages content in a local authenticated browser session and expects the user to review and manually publish.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
