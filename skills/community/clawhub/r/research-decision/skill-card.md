## Description: <br>
Research Decision helps agents perform bilingual web research, cross-check high-quality sources, and turn evidence into decisions, troubleshooting guidance, risk notes, and next steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Krishnna2725](https://clawhub.ai/user/Krishnna2725) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and technical decision makers use this skill when they need evidence-based recommendations for technology selection, upgrades, compatibility questions, production readiness, known issues, or difficult bug triage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research queries and read-only local checks may reveal sensitive project names, incident details, dependency versions, or software inventory. <br>
Mitigation: Use generalized external search terms for confidential topics and ask before inspecting local environments that may contain sensitive context. <br>


## Reference(s): <br>
- [Query Patterns](references/query-patterns.md) <br>
- [Issue Triage](references/issue-triage.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown research report with cited conclusions, risk notes, and actionable next steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include read-only environment or dependency check commands when they help verify a version, dependency, or troubleshooting claim.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
