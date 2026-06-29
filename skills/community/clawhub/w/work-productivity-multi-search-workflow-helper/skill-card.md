## Description: <br>
Coordinate multi-source web and repository search. Use when the user needs query expansion, source diversity, deduped findings, evidence grading, citation planning, or a repeatable search workflow across search engines, forums, docs, code hosts, and registries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyro-ma](https://clawhub.ai/user/kyro-ma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
AI-agent users, skill authors, maintainers, and teams use this skill to plan source-diverse searches, deduplicate findings, grade evidence quality, and produce concise research syntheses with audit-ready links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger wording may activate the skill for loosely related search or bug-fix requests. <br>
Mitigation: Review the proposed search plan and scope before allowing broad external searches. <br>
Risk: External searches can expose private or sensitive context if the user includes it in queries. <br>
Mitigation: Redact sensitive details and prefer generalized query variants unless disclosure is intentional. <br>
Risk: Repeated copies of the same source or anecdotal posts can make evidence appear stronger than it is. <br>
Mitigation: Deduplicate sources, label weak evidence, and distinguish confirmed facts from plausible leads. <br>


## Reference(s): <br>
- [Requirement Plan](artifact/references/requirement-plan.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/work-productivity-multi-search-workflow-helper) <br>
- [Multi Search Engine Demand Signal](https://clawhub.ai/skills/multi-search-engine) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown search plans, evidence lists, source matrices, recommendations, and reusable query sets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves links, labels weak evidence, and calls out stale or duplicated sources when available] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
