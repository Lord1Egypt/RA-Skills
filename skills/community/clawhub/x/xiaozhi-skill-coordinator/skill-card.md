## Description: <br>
Coordinates Xiaozhi learning skills so mistake reviews, Feynman checks, Cornell notes, learning plans, and focus data can support scoped learning analysis, monthly reports, system health checks, and handoffs with user consent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qizhitang](https://clawhub.ai/user/qizhitang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, tutors, and learning-support agents use this skill to coordinate multiple Xiaozhi learning skills for mistake analysis, full-system monthly reports, learning-system health checks, and consent-scoped profile or reminder handoffs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cross-skill coordination can expose more learning history than a single task needs. <br>
Mitigation: Query only the minimum summary fields needed for the current user-requested analysis, report, or health check. <br>
Risk: Profile writebacks or reminder creation can change a learner's ongoing study system without clear consent. <br>
Mitigation: Confirm user authorization before writing profile summaries or syncing reminders, and allow the user to exclude specific skills or writebacks. <br>
Risk: Malformed handoff data could pollute downstream learner profiles or interrupt multi-agent coordination. <br>
Mitigation: Validate handoff, profile writeback, and reminder payloads against the bundled protocol schema, block malformed writes, and fall back to single-session text diagnosis when validation fails. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qizhitang/xiaozhi-skill-coordinator) <br>
- [Publisher profile](https://clawhub.ai/user/qizhitang) <br>
- [One-week linkage record](references/one-week-linkage-record.md) <br>
- [Handover protocol schema](schemas/handover-protocol.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional schema-constrained JSON handoff blocks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should use only task-needed summaries, respect user consent before cross-skill access, and validate handoff or writeback data against the bundled schema.] <br>

## Skill Version(s): <br>
1.1.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
