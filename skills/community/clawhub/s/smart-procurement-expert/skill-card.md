## Description:

A Chinese procurement and bidding workflow assistant for bidder-side opportunity screening, bid planning, tender analysis, response drafting, consistency review, scoring support, challenge handling, and post-bid knowledge capture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

External procurement, bid, and compliance teams use this skill to navigate Chinese bidding and government-procurement workflows, generate structured draft materials, calculate price scores from reviewed rules, and flag legal or submission risks for human confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency and local file-handling cautions apply to the document parsing, repair, and generation utilities.

Mitigation: Use pinned, reviewed versions of python-docx, pypdf, and docx where possible; keep backups of source bid documents; and prefer explicit output paths for repair scripts.

Risk: Pricing, legal, and final-submission outputs can materially affect bid outcomes or compliance obligations.

Mitigation: Manually verify pricing calculations, legal conclusions, complaint decisions, and final-submission materials before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chesaram/skills/smart-procurement-expert)
- [两法分轨判定（Step0 必读）](references/legal-domains.md)
- [知识库联动设计](references/kb-linkage.md)
- [商机甄别与投标决策方法论](references/opportunity-screening.md)
- [应标任务分解方法论](references/task-decomposition.md)
- [评分建模方法论（借鉴并优化）](references/scoring-model.md)
- [价格分规则半自动抽取（深度节点 C 上游工具）](references/price-rule-extraction.md)
- [响应文件生成方法论（深度节点 B）](references/docx-generation.md)
- [响应文件内容自动填充（深度节点 B 编排层）](references/response-autofill.md)
- [文稿润色与去模板化方法论](references/document-polish.md)
- [图表占位与可视化增强方法论](references/chart-placeholder.md)
- [呈交终审方法论](references/final-review.md)
- [一致性审查方法论（深度节点 A）](references/consistency-check.md)
- [前沿适配专章（跨节点引用）](references/frontier-adaptation.md)
- [经验沉淀与知识复用方法论](references/experience-crystallization.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese Markdown guidance, structured checklists, JSON configuration drafts, shell command examples, and editable document-generation outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs that affect pricing, legal interpretation, bid/no-bid decisions, complaints, or final submission require manual verification.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
