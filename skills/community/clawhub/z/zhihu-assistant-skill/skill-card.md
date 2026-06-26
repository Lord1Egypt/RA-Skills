## Description: <br>
Fetches Zhihu hot-list topics, generates AI answer drafts, and sends drafts to Feishu for human review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[naiveKid](https://clawhub.ai/user/naiveKid) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to monitor Zhihu trending questions, draft candidate answers with an AI model, deduplicate previously handled topics, and route drafts through a Feishu-based human review queue before publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Zhihu session cookie and AI API keys, which are sensitive account credentials. <br>
Mitigation: Use a low-risk account where possible, store secrets only through the expected configuration mechanism, and avoid exposing them in shell history, logs, or shared files. <br>
Risk: Generated answer drafts and review queue data may persist in the skill workspace. <br>
Mitigation: Review workspace storage access, remove stale drafts when no longer needed, and treat stored queue and audit files as potentially sensitive. <br>
Risk: AI-generated drafts may be inaccurate, low quality, or unsuitable for publication. <br>
Mitigation: Keep the documented human review step before posting content and verify that final content follows Zhihu community rules. <br>
Risk: Installing dependencies directly into a shared Python environment can affect other tools. <br>
Mitigation: Install and run the skill in an isolated Python environment when practical. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/naiveKid/zhihu-assistant-skill) <br>
- [Kimi Open Platform](https://platform.moonshot.cn/) <br>
- [Moonshot API base URL](https://api.moonshot.cn/v1) <br>
- [Zhihu hot-list API endpoint](https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, API calls, Guidance] <br>
**Output Format:** [Markdown-style answer drafts, CLI status text, JSON queue and memory files, logs, and Feishu notification messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Drafts are intended for human review before publication; queue, memory, and audit data remain in the skill workspace.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
