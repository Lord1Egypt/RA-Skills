## Description: <br>
Generates structured Chinese AI industry news digests by searching current AI news and summarizing key developments, funding, product launches, and technical breakthroughs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yqghlx](https://clawhub.ai/user/yqghlx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teams, analysts, and developers use this skill to monitor current AI industry news, track specific AI topics or company activity, and produce daily or weekly Chinese briefings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill searches and fetches web pages for current news, so query terms and selected sources may leave the agent environment. <br>
Mitigation: Use non-sensitive topics and review source links before relying on the digest. <br>
Risk: News summaries may be incomplete, stale, or affected by source quality. <br>
Mitigation: Ask for cited sources and verify important claims against authoritative publications. <br>
Risk: When Feishu output is requested, the skill can create and write a document outside the chat. <br>
Mitigation: Request Feishu output only when document creation is intended, and review the resulting document before sharing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yqghlx/test-pub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text, with an optional Feishu document link when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to Chinese output, includes source links for news items, and supports user-specified topic, language, format, and detail preferences.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
