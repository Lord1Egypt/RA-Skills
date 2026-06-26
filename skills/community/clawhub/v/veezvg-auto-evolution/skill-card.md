## Description: <br>
Builds and maintains a self-evolving agent skill system that captures corrective feedback, graduates repeated feedback into rule proposals, improves low-performing skills, and proposes new skills when repeated patterns are not covered. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[veezvg](https://clawhub.ai/user/veezvg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture corrective feedback, aggregate repeated issues, and present user-confirmed proposals for rule graduation, skill improvement, or new skill creation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic feedback capture may save user corrections or sensitive context to local feedback files without clear opt-in. <br>
Mitigation: Disclose the capture behavior before enabling it, redact secrets and personal data, and limit saved content to the minimum needed for feedback analysis. <br>
Risk: Accumulated feedback records may persist longer than intended or be readable by unintended local users. <br>
Mitigation: Restrict access to `.claude/feedback/` and define review, deletion, and retention controls before deployment. <br>
Risk: Repeated feedback could be promoted into rules or skill changes incorrectly if proposals are accepted without review. <br>
Mitigation: Require a user or maintainer to review each proposal, target file, and rationale before applying any rule or skill change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/veezvg/veezvg-auto-evolution) <br>
- [README](artifact/README.md) <br>
- [Reference Architecture](artifact/REFERENCE_ARCHITECTURE.md) <br>
- [Examples](artifact/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-style proposals with optional shell commands and file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces suggestions and structured feedback records; rule or skill changes require user confirmation.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
