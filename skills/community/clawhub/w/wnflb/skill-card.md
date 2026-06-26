## Description: <br>
获取福利吧 (https://www.wnflb2023.com/) 指定板块的帖子列表（标题、内容、链接），进入帖子提取正文内容，最后由 AI 归纳总结。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nsnake](https://clawhub.ai/user/nsnake) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to fetch recent posts from selected 福利吧 forum sections, summarize thread content, and extract useful links or passwords into a Markdown table. It can also run a forum check-in action for the configured account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a 福利吧 forum session cookie and can persist updated cookie values. <br>
Mitigation: Use a throwaway or low-privilege forum account, restrict cookie.txt permissions, and do not ask the agent to display cookie.txt contents. <br>
Risk: The check-in command performs an account action using the configured session. <br>
Mitigation: Run the check-in command only when the user explicitly intends that account action. <br>
Risk: The scraper follows redirects while sending a session cookie. <br>
Mitigation: Review or patch the code to enforce a www.wnflb2023.com origin allowlist before sending or persisting cookies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nsnake/wnflb) <br>
- [福利吧 forum](https://www.wnflb2023.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries with JSON command output from the scraper/check-in script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The scraper returns forum title, source URL, section ID, item count, and thread items containing title, URL, and content; summaries should stay under 200 Chinese characters per item.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
