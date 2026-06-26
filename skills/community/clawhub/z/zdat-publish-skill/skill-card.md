## Description: <br>
ZDAT Publish Skill helps agents adapt, schedule, dispatch, and log content publishing across TouTiao, WeChat Official Accounts, Zhihu, Xiaohongshu, Weibo, Douyin, and Video Accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freemanyg](https://clawhub.ai/user/freemanyg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators and developers use this skill to prepare platform-specific post formats, invoke the local ZDAT publishing engine, schedule dispatches, and review publish logs across supported Chinese social platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide automated publishing or scheduling to live social platforms. <br>
Mitigation: Require explicit human review and confirmation before any post is published or scheduled. <br>
Risk: The skill includes guidance to avoid AI or originality detection. <br>
Mitigation: Do not use evasion guidance; require content to comply with platform policies and disclosure requirements. <br>
Risk: The publishing scripts depend on a local engine path, workspace configuration, and publishing logs. <br>
Mitigation: Verify the local publishing engine, WORKDIR, platform rules, and log destination before running scripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freemanyg/zdat-publish-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and Python script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read platform rules from WORKDIR and display publish status or log summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
