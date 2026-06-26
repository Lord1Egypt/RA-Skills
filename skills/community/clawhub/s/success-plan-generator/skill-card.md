## Description: <br>
Generates B2B customer success plan drafts with milestones, verifiable outcomes, review rhythms, ownership, and renewal signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Customer success and account teams use this skill to turn customer goals, milestones, and resource constraints into review-ready B2B success plans for QBR preparation, renewal planning, and implementation alignment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled Python helper includes local audit and scanning behavior outside the core success-plan drafting use case. <br>
Mitigation: Review the helper before installation and invoke it only with explicit, narrow input files. <br>
Risk: Customer inputs may include sensitive account, commercial, or personal information. <br>
Mitigation: Remove or minimize sensitive details before use and review generated plans before sharing or entering them into customer systems. <br>
Risk: A generated success plan could be mistaken for a contractual commitment or formal project plan. <br>
Mitigation: Treat outputs as review drafts, confirm missing facts, and validate commitments against the governing contract or project process. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/52YuanChangXing/success-plan-generator) <br>
- [Publisher Profile](https://clawhub.ai/user/52YuanChangXing) <br>
- [README](artifact/README.md) <br>
- [Specification](artifact/resources/spec.json) <br>
- [Output Template](artifact/resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Markdown draft, or JSON when the optional helper is invoked with JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Review-ready output that lists missing information for confirmation; the optional Python helper reads explicit input and can write a Markdown or JSON report.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
