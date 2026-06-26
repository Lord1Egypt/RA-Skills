## Description: <br>
Guides an agent through a fixed Xiaohongshu publishing workflow to improve posting success. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuchenggong19851114-design](https://clawhub.ai/user/zhuchenggong19851114-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators or operators use this skill to have an agent publish confirmed Xiaohongshu content through a logged-in creator browser session and report success or a retry reason. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may make an unintended public post from an authenticated Xiaohongshu creator session. <br>
Mitigation: Before any final publish action, review the target account, text, generated image or uploaded media, title, tags, and any Feishu recording step. <br>
Risk: The skill depends on an already logged-in browser session. <br>
Mitigation: Use it only when you are comfortable allowing the agent to operate that creator session, and ask the user to re-authenticate if the session has expired. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhuchenggong19851114-design/xiaohongshu-create) <br>
- [Xiaohongshu creator image publish page](https://creator.xiaohongshu.com/publish/publish?target=image) <br>
- [Xiaohongshu creator long-form publish page](https://creator.xiaohongshu.com/publish/publish?target=text) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text] <br>
**Output Format:** [Plain text or Markdown status with a success link, failure reason, and retry guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a Xiaohongshu post link when publishing succeeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
