## Description: <br>
Registry Sync keeps a Feishu registry sheet current when agents create or significantly update local skills, workflows, templates, or content flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[G-Hanasq](https://clawhub.ai/user/G-Hanasq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to keep a Feishu-based registry aligned with newly created or materially updated local skills, reusable workflows, templates, and content-related flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may update a specific Feishu registry sheet automatically after local skills, workflows, templates, or content flows change. <br>
Mitigation: Confirm the sheet is appropriate for the data, keep Feishu permissions scoped, and review direct or queued registry changes. <br>
Risk: If Feishu Sheets is unavailable, pending registry details may be written to a local backlog file. <br>
Mitigation: Avoid placing sensitive internal details in queued backlog entries and review the backlog before syncing it. <br>


## Reference(s): <br>
- [Registry Sync source](artifact/SKILL.md) <br>
- [ClawHub release page](https://clawhub.ai/G-Hanasq/registry-sync) <br>
- [Configured Feishu registry sheet](https://bytedance.larkoffice.com/sheets/Bf6qsMV9fhqrD6tPE6TcQhF7nEe) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Guidance] <br>
**Output Format:** [Concise Markdown confirmation; registry rows or backlog entries as needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update the configured Feishu sheet or queue a local backlog entry when the sheet is unavailable.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
