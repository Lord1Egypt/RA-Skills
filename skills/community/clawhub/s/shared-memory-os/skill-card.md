## Description: <br>
Shared memory governance for multi-agent OpenClaw workspaces with tiered memory, learnings capture, promotion review, lifecycle management, self-maintaining reports, cross-skill collaboration, and bilingual ClawHub-friendly docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zqh2333](https://clawhub.ai/user/zqh2333) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent-workspace maintainers use this skill to organize shared memory, harvest reusable learnings, review promotion candidates, detect stale or duplicate memory, and generate maintenance reports for multi-agent OpenClaw workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup can create recurring automated OpenClaw maintenance jobs with exec/read access. <br>
Mitigation: Install only when recurring maintenance is intentional, review the three jobs before enabling them, and document how to disable or remove the jobs. <br>
Risk: Scripts are hard-coded to one local workspace path. <br>
Mitigation: Verify the target workspace path before running setup or maintenance scripts, and adjust the path for the intended workspace before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zqh2333/shared-memory-os) <br>
- [Governance Guide](references/governance-guide.md) <br>
- [Health Check Guide](references/health-check.md) <br>
- [Migration Playbook](references/migration-playbook.md) <br>
- [Skill Intake Protocol](references/skill-intake-protocol.md) <br>
- [Cross-Skill Collaboration](references/cross-skill-collaboration.md) <br>
- [Auto-Sync Checklist](references/auto-sync-checklist.md) <br>
- [Release State](references/release-state.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, JSON reports, shell commands, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update workspace memory files, reports, indexes, and recurring maintenance job configuration when the user runs setup or maintenance scripts.] <br>

## Skill Version(s): <br>
1.7.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
