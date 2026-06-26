## Description: <br>
微信潜在客户抓取、分析与自动回复营销自动化技能 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ling-qian](https://clawhub.ai/user/ling-qian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, marketing, and community operations users can use this skill to identify WeChat contacts or conversations that may represent leads, score them, and draft follow-up messages for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process identifiable WeChat conversation data without adequate consent or user-control safeguards. <br>
Mitigation: Complete a privacy and compliance review before installation, and only process conversations when authorization is documented. <br>
Risk: Real WeChat cookies and scheduled scans could broaden collection beyond intended contacts or conversations. <br>
Mitigation: Do not connect a real WeChat cookie or enable scheduled scanning until the approved scope, access controls, and deletion process are in place. <br>
Risk: Raw messages, names, and lead profiles can be retained in output files or agentmemory. <br>
Mitigation: Avoid storing raw messages or names where possible, restrict output access, and define how to delete generated files and clear agentmemory entries. <br>
Risk: Auto-reply behavior can send marketing follow-ups before human review. <br>
Mitigation: Keep auto-reply disabled by default and review generated reply drafts before any message is sent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ling-qian/wechat-lead-generation) <br>
- [ClawDIS homepage](https://github.com/ling-qian/openclaw-skills/tree/main/wechat-lead-generation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON profile artifacts, Markdown reply drafts, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May store lead profiles and chat-derived details in local output files and agentmemory when enabled.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
