## Description: <br>
Analyzes living-room camera audio and video to estimate family or couple conflict intensity as low, medium, or high and generate reminders or report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, family counselors, and mediation or smart-home operators use this skill to analyze consented living-room audio/video or URLs for conflict-intensity indicators, gentle reminders, and historical report summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles highly sensitive family audio/video and may send media or links to backend services for processing. <br>
Mitigation: Install and run it only after reviewing the provider, consent model, retention policy, and access controls; use consented inputs and avoid long-term raw media storage. <br>
Risk: Account identity, tokens, personal details, and report history may be associated with analyses. <br>
Mitigation: Review local token and configuration storage, restrict access to report-history lookup, and remove credentials or cached state when the skill is no longer needed. <br>
Risk: Conflict-intensity outputs could be misused as legal, psychological, or domestic-violence determinations. <br>
Mitigation: Treat outputs as acoustic and visual indicators with gentle reminders only; do not use them to label people or replace legal, clinical, or safety judgment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-family-conflict-intensity-detect-analysis) <br>
- [API documentation](references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown tables or JSON analysis reports with report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save analysis output to a user-specified file and can list historical reports.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter lists 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
