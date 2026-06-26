## Description: <br>
Uses Playwright to help an agent back up Weibo favorites, personal posts, or other users' posts, including images, optional videos, long articles, and Markdown navigation links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hhjin](https://clawhub.ai/user/hhjin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run a local Playwright workflow that archives authorized Weibo favorites, personal timelines, or selected public profiles into Markdown with local media folders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can save reusable Weibo login cookies and browser profile data locally. <br>
Mitigation: Use a dedicated browser profile and protect or delete cookies.json and browser_data after use. <br>
Risk: Browser-session access can expose more account state than the intended backup task requires. <br>
Mitigation: Set a clear target URL and download limit, and only archive content you are authorized to retain. <br>
Risk: The --connect-browser option can control an already-running browser session. <br>
Mitigation: Avoid --connect-browser unless the operator understands the browser-control risk and has isolated the session. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hhjin/weibo-backup) <br>
- [Publisher Profile](https://clawhub.ai/user/hhjin) <br>
- [ModelScope Skill Page](https://www.modelscope.cn/skills/hhjinhh/weibo-data-backup) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Files] <br>
**Output Format:** [Markdown guidance with bash commands; downloaded Weibo content is saved as Markdown files with local media directories.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create cookies.json, browser_data, output/pictures, output/videos, and output/articles under the skill or chosen output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
