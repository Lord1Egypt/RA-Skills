## Description: <br>
Drafts stakeholder updates from the same project facts for bosses, clients, execution teams, and risk-transparent communication workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and project teams use this skill to turn project progress, risks, and next steps into reviewable Markdown updates tailored for management, clients, execution teams, and transparent risk reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local helper processes files selected by the user and can write to a user-specified output path. <br>
Mitigation: Use only appropriate project materials, avoid sensitive inputs unless approved for stakeholder updates, and review the generated file before sharing. <br>
Risk: Dormant audit helpers in the shipped script may create ambiguity about the skill's behavior. <br>
Mitigation: Publisher should document or remove dormant audit helpers; users should rely on the documented stakeholder-update workflow. <br>
Risk: Stakeholder updates can become misleading if risks or missing facts are omitted. <br>
Mitigation: Keep risk-transparent sections and待确认项 in the draft, and confirm missing facts before sending or publishing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/52YuanChangXing/stakeholder-update-drafter) <br>
- [README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Output Template](artifact/resources/template.md) <br>
- [Structured Specification](artifact/resources/spec.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Markdown draft or JSON wrapper containing a Markdown report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a local output file when the optional Python helper is run with an output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
