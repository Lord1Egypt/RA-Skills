## Description: <br>
Detects child hazardous behaviors such as climbing, playing with fire, touching power sources, and dangerous actions near windows, then returns structured safety reports and alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, caregivers, school safety staff, and developers use this skill to analyze child-monitoring media for hazardous behaviors and to retrieve account-linked history reports. It is an assistance tool; alerts should be confirmed by a responsible adult before intervention decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Child-monitoring videos or URLs are sent to the LifeEmergence cloud service for analysis. <br>
Mitigation: Use only with appropriate consent and policy approval; clarify retention, deletion, and data-handling requirements before using real footage of minors. <br>
Risk: The skill silently creates or reuses a local identity and retrieves account-linked history reports. <br>
Mitigation: Review account scoping before installation and ensure report links or identity-linked outputs are shared only with authorized users. <br>
Risk: Local workspace storage may contain tokens or identity data used for cloud API access. <br>
Mitigation: Install only in workspaces with appropriate access controls and clear local credentials when the skill is no longer needed. <br>
Risk: Behavior detection alerts can be incomplete or incorrect. <br>
Mitigation: Treat outputs as child-safety supervision assistance and verify alerts directly before taking action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-child-dangerous-behavior-recognition-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API documentation](references/api_doc.md) <br>
- [Shared analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown and JSON analysis reports, with optional saved text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports local video files or public video URLs, configurable alert threshold, basic/standard/json detail levels, and Markdown tables for history reports.] <br>

## Skill Version(s): <br>
1.0.5 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
