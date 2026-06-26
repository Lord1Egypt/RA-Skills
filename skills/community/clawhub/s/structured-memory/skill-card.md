## Description: <br>
Build and maintain a structured memory system for OpenClaw workspaces using layered storage: daily memory as the source of truth, domain/module/entity/tag indexing, critical-facts extraction, and retrieval planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChauncyZBC](https://clawhub.ai/user/ChauncyZBC) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to initialize, update, and retrieve from a layered workspace memory system that scales across business, finance, legal, HR, project, operations, technology, routines, and personal context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist sensitive workspace memory facts into long-lived memory indexes and critical-fact files. <br>
Mitigation: Avoid storing secrets in daily memory, follow the critical-facts policy, and review memory outputs before relying on or sharing them. <br>
Risk: First-run backfill and rebuild scripts can broadly update derived memory files. <br>
Mitigation: Run the scripts only in the intended workspace, review generated changes, and verify custom output paths before use. <br>


## Reference(s): <br>
- [Taxonomy](references/taxonomy.md) <br>
- [Write Rules](references/write-rules.md) <br>
- [Retrieval Planner](references/retrieval-planner.md) <br>
- [Index Schema](references/index-schema.md) <br>
- [Critical Facts Policy](references/critical-facts-policy.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, JSON, Files] <br>
**Output Format:** [Markdown guidance with bash commands, plus generated JSON indexes and Markdown memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains daily-memory-derived indexes, module and entity files, critical-fact files, and object-style fact cards.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md, README.md, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
