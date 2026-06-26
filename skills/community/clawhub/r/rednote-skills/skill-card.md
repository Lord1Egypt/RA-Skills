## Description: <br>
Comprehensive tool for interacting with the rednote (xiaohongshu,小红书) platform that enables users to search for posts by keyword, extract content from specific notes in markdown format, and perform interaction actions like liking, commenting, collecting, following, and publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MrMao007](https://clawhub.ai/user/MrMao007) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users can use this skill to automate Rednote/Xiaohongshu workflows, including searching for notes, extracting note content, and performing account actions such as publishing, commenting, following, liking, and collecting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reuse saved Rednote/Xiaohongshu login cookies to act on a user's account. <br>
Mitigation: Keep rednote_cookies.json private, delete or revoke it when work is complete, and limit access to the workspace where the cookie file is stored. <br>
Risk: The skill can publish, comment, follow, like, collect, and upload local images without built-in confirmation checks. <br>
Mitigation: Require explicit user approval before any visible account action or local image upload is executed. <br>
Risk: Browser automation depends on current Xiaohongshu page structure and may fail if the site UI changes or access is restricted. <br>
Mitigation: Validate login and test the target workflow before relying on results; inspect failures before retrying account actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MrMao007/rednote-skills) <br>
- [Xiaohongshu](https://www.xiaohongshu.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, strings, and command-line output from Playwright automation scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create and reuse rednote_cookies.json for authenticated browser sessions.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
