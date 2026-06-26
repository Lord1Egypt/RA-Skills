## Description: <br>
A Chinese-language meta-domain payload that organizes human activities into five needs, six universal operations, twelve life domains, and cross-domain value chains for UTOS-assisted planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent builders use this skill as a broad reference and orchestration payload for life-domain planning across health, wealth, education, career, family, social, legal, technology, creative, civic, spiritual, and life-operations workflows. It is intended to define domain relationships, task catalogs, requirements, exemplars, and calibration points that another orchestration skill can consume. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to automatically install universal-task-os. <br>
Mitigation: Disable automatic installation or require explicit user confirmation before installing or loading additional skills. <br>
Risk: The payload covers high-stakes health, legal, financial, and civic workflows. <br>
Mitigation: Treat outputs in these domains as drafts and require review by qualified professionals or responsible humans before action. <br>
Risk: Civic and opinion-oriented workflows could be misused for deceptive amplification, harassment, or unreviewed publishing. <br>
Mitigation: Require human approval before publication or outreach and prohibit deceptive amplification and harassment use cases. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangjiaocheng/ultimate-domain-payload) <br>
- [SKILL.md](SKILL.md) <br>
- [D01 Health domain payload](references/D01-health-SKILL.md) <br>
- [D02 Wealth domain payload](references/D02-wealth-SKILL.md) <br>
- [D03 Education domain payload](references/D03-education-SKILL.md) <br>
- [D04 Career domain payload](references/D04-career-SKILL.md) <br>
- [D05 Family domain payload](references/D05-family-SKILL.md) <br>
- [D06 Social domain payload](references/D06-social-SKILL.md) <br>
- [D07 Legal domain payload](references/D07-legal-SKILL.md) <br>
- [D08 Technology domain payload](references/D08-tech-SKILL.md) <br>
- [D09 Creative domain payload](references/D09-creative-SKILL.md) <br>
- [D10 Civic domain payload](references/D10-civic-SKILL.md) <br>
- [D11 Spiritual domain payload](references/D11-spiritual-SKILL.md) <br>
- [D12 Life operations domain payload](references/D12-life-ops-SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance and structured domain-reference text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on Universal Task OS for execution; without that dependency the skill functions as read-only reference material.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
