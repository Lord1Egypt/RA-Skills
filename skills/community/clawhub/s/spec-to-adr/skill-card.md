## Description: <br>
Convert agent execution plans into MADR-format Architecture Decision Records for audit trails and architecture progression. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rawc0der](https://clawhub.ai/user/rawc0der) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to convert implementation plans, GSD phase plans, Cursor CreatePlan files, or generic markdown plans into numbered MADR Architecture Decision Records and maintain an ADR index. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads project plan files and writes ADR documentation in the repository, which can introduce incorrect or misleading architectural records if the source plan is incomplete or misread. <br>
Mitigation: Use a branch and review the generated ADR and README changes before committing. <br>
Risk: Superseding an older ADR can alter the documented decision history if the target ADR number or relationship is wrong. <br>
Mitigation: Review superseded ADR status changes and confirm the new ADR number before merging. <br>


## Reference(s): <br>
- [MADR Template](references/madr-template.md) <br>
- [ADR Index Template](assets/adr-index-template.md) <br>
- [MADR Format](https://adr.github.io/madr/) <br>
- [ClawHub Skill Page](https://clawhub.ai/rawc0der/spec-to-adr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown ADR files and a markdown ADR index, with a short text summary to the user] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates repository documentation under the detected ADR directory convention.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
