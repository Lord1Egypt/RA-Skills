## Description: <br>
微信智能管家：自动回复、消息分类、聊天记录分析、联系人管理。Trigger on: 微信, WeChat, 群聊, 朋友圈, 公众号, 聊天记录, 联系人, 表情包, 小程序, 红包. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawto](https://clawhub.ai/user/clawto) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to manage WeChat-derived messages, contacts, auto-reply rules, and chat analytics through configured WeChat or openclaw-weixin integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles private WeChat messages, contact data, monitoring workflows, and auto-reply rules. <br>
Mitigation: Install only in trusted agent sessions, use a dedicated account or workspace, and review openclaw-weixin permissions before enabling access. <br>
Risk: Auto-reply rules can send account actions on the user's behalf. <br>
Mitigation: Review and approve auto-reply rules explicitly before use, especially for shared, business, or sensitive conversations. <br>
Risk: Message and contact data may expose sensitive personal or business information. <br>
Mitigation: Avoid shared agent sessions and limit retained WeChat-derived data to what is needed for the intended workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clawto/wechat-manager) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and command-line text with configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize or act on cached WeChat messages, contacts, extracted links, todos, addresses, and auto-reply rules.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
