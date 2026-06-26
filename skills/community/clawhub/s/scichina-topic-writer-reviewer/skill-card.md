## Description: <br>
科普智创审校助手。当用户提到「科普中国热点创作」「科普工作」「热点采集与科普写作」或类似意图时激活。执行以下流程：(1) 监控 kepuchina.cn 整理热门文章与关键字；(2) 根据关键字为用户拟写科普文章；(3) 执行科学性审查与引用来源核查，防止大模型幻觉。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binhuatochina](https://clawhub.ai/user/binhuatochina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Science communication writers and editors use this skill to gather recent Kepu China topics, draft public-facing science articles, verify claims and references, and prepare reviewed content for Feishu publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can create and share Feishu documents and retain document links locally. <br>
Mitigation: Confirm the Feishu workspace, parent node, account, sharing permissions, content format, and local link-retention behavior before running the full workflow; use preview-only mode when remote document creation is not desired. <br>
Risk: Science or health article drafts can include incorrect facts, unverifiable claims, or fabricated references if review steps are skipped. <br>
Mitigation: Require the built-in scientific review, citation verification, and fact-checking steps before publishing or writing content to Feishu. <br>


## Reference(s): <br>
- [科普中国](https://www.kepuchina.cn/) <br>
- [ClawHub skill page](https://clawhub.ai/binhuatochina/scichina-topic-writer-reviewer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown article draft, reference list, review report, Feishu document link, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a Feishu document and record the resulting document link locally when the full workflow is run.] <br>

## Skill Version(s): <br>
0.1.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
