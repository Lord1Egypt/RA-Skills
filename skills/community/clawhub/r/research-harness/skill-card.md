## Description: <br>
Research Harness routes public-market research tasks through structured workflows for company deep dives, industry maps, earnings previews, consensus checks, red-team reviews, and PM-ready briefs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joansongjr](https://clawhub.ai/user/joansongjr) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External analysts, fund managers, and research teams use this skill to structure AI-assisted public-market research across A-shares, Hong Kong stocks, U.S. equities, funds, and cross-market themes. It emphasizes evidence grading, source planning, checkpoints, archiving, and compliance boundaries for repeatable research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist research targets, notes, checkpoints, task state, and full outputs in local workspace files. <br>
Mitigation: Use a private workspace for sensitive work, avoid shared directories, and periodically review .task-pulse, .checkpoint, active-tasks.md, biases.md, and archived outputs. <br>
Risk: Auto-triggering and routing can start multi-step research workflows that use available data sources and produce archived outputs. <br>
Mitigation: Review the preflight plan, selected workflow, data-source choices, and archive paths before relying on or retaining generated research. <br>
Risk: Financial research outputs can be mistaken for investment advice or final analyst judgment. <br>
Mitigation: Apply the bundled compliance boundaries: do not treat outputs as buy or sell instructions, and require human review for ratings, target prices, earnings forecast changes, and client-facing conclusions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/joansongjr/research-harness) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/joansongjr) <br>
- [Evidence Grading](core/evidence.md) <br>
- [Compliance Boundaries](core/compliance.md) <br>
- [Data Adapters](core/adapters.md) <br>
- [Output Archive](core/output-archive.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown research outputs with structured checklists, tables, source plans, evidence labels, and archive paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local research notes, checkpoints, task state, and archived Markdown outputs when used in a configured workspace.] <br>

## Skill Version(s): <br>
0.7.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
