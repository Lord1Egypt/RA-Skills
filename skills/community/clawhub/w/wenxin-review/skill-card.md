## Description: <br>
文心审 is a Chinese humanities-paper reading assistant for graduate students in literature, history, philosophy, linguistics, and related fields, producing an eight-dimension structured review that cites source locations and separates author claims from reading judgments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuzliya](https://clawhub.ai/user/yuzliya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Graduate students and humanities researchers use this skill to deeply read, critique, and review Chinese academic papers. It helps them assess research questions, evidence strength, methodological reproducibility, related-work positioning, argument robustness, and the gap between narrative claims and actual contribution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reviewing a local PDF path or URL may expose the selected document or page contents to the agent during analysis. <br>
Mitigation: Provide only documents and URLs that are appropriate for the active agent environment, and review the generated critique before relying on it. <br>
Risk: A structured humanities review can still contain mistaken judgments about evidence strength, citations, or disciplinary context. <br>
Mitigation: Use the report as an aid to reading and verify important claims against the original paper and relevant source material. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/yuzliya/wenxin-review) <br>
- [人文学科审稿参考：常见论证漏洞模式](references/common-fallacies.md) <br>
- [人文学科审稿参考：学科差异速查](references/discipline-differences.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown structured review report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Eight-dimension review with source-location annotations, evidence-strength labels, a final assessment, and a reading recommendation.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
