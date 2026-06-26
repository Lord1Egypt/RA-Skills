## Description: <br>
小红书相关操作，覆盖账号定位、选题研究、内容生产、发布执行与复盘修复的小红书全链路运营技能。凡是小红书的浏览/搜索/发布/评论任务，默认必须使用 OpenClaw 内置浏览器流程并指定 profile="openclaw"；除非用户明确要求，否则不要使用系统 open 或外部浏览器。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiangyu-cas](https://clawhub.ai/user/xiangyu-cas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, operators, and agent users use this skill to support Xiaohongshu account operations, including account positioning, feed and competitor research, topic ideation, copy drafting, publish-page preparation, comment handling, and local knowledge-base capture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act through a logged-in Xiaohongshu browser profile. <br>
Mitigation: Use a dedicated account or browser profile, keep publish and reply actions user-confirmed, and stop at the publish button unless the user explicitly approves. <br>
Risk: The skill may persist account, feed, comment, or operational observations into a local knowledge base. <br>
Mitigation: Review knowledge-base entries before retaining or sharing them, and ask the agent not to write the knowledge base unless storage is approved. <br>
Risk: The skill may share screenshots or page data through Feishu when confirmation workflows use attachments. <br>
Mitigation: Only allow screenshot sharing after choosing the recipient and confirming that the page data is appropriate to send. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xiangyu-cas/xiaohongshu-ops) <br>
- [OpenClaw browser tool documentation](https://docs.openclaw.ai/tools/browser) <br>
- [XHS runtime rules](references/xhs-runtime-rules.md) <br>
- [XHS account analysis](references/xhs-account-analysis.md) <br>
- [XHS home feed analysis](references/xhs-home-feed-analysis.md) <br>
- [XHS topic ideation](references/xhs-topic-ideation.md) <br>
- [XHS publish flows](references/xhs-publish-flows.md) <br>
- [XHS comment ops](references/xhs-comment-ops.md) <br>
- [XHS viral copy flow](references/xhs-viral-copy-flow.md) <br>
- [XHS knowledge base](references/xhs-knowledge-base.md) <br>
- [XHS evaluation patterns](references/xhs-eval-patterns.md) <br>
- [Knowledge base overview](knowledge-base/README.md) <br>
- [Skill smoke test](testcase.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and structured prose, with occasional code-like snippets or shell commands for browser and tool steps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can prepare publish-ready social copy, reply drafts, analysis summaries, and local knowledge-base entries; public posts, replies, and external sharing should remain user-confirmed.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
