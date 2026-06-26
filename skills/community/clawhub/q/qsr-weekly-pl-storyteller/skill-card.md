## Description: <br>
Turns weekly restaurant KPIs into a plain-English financial narrative about what happened, why it matters, and what to do next. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mcphersonai](https://clawhub.ai/user/mcphersonai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Restaurant and franchise operators use this skill to turn weekly sales, labor, food cost, traffic, catering, waste, and overtime metrics into a concise operating narrative. It supports weekly reviews, trend comparisons, monthly rollups, and one recommended focus item for the next week. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store restaurant financial and operational metrics in agent memory for trend comparisons. <br>
Mitigation: Use anonymized or minimum-needed numbers where possible, and review the agent platform's memory controls so confidential reports can be deleted or kept out of long-term memory. <br>
Risk: Generated P&L narratives and recommendations may be wrong if weekly inputs are incomplete, mistyped, or missing business context. <br>
Mitigation: Review the source KPI values and treat the focus recommendation as decision support rather than a substitute for operator judgment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mcphersonai/qsr-weekly-pl-storyteller) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown narrative report with KPI summary, trend comparison, and one focus recommendation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses operator-supplied restaurant metrics and can build a running weekly archive when memory is enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
