## Description: <br>
ZF-novel-writer helps OpenClaw agents plan, draft, quality-check, and archive long-form novel chapters with continuity tracking and outline-driven workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangfeixia0101](https://clawhub.ai/user/huangfeixia0101) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External authors and creative-writing agents use this skill to manage a multi-agent novel-writing workflow: outline-driven chapter planning, chapter drafting, quality checks, and continuity updates across a long-form project. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run broad automated agent and file-writing workflows with weak scoping and unclear user control. <br>
Mitigation: Use it only in a dedicated project directory, invoke it explicitly, and review generated file paths and planned actions before allowing helper scripts or agents to modify files. <br>
Risk: Novel drafts, outlines, and continuity files may persist locally and could contain sensitive manuscript content. <br>
Mitigation: Avoid using the workflow on sensitive manuscripts unless local prompt and file retention is acceptable, and review generated continuity files before sharing or publishing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/huangfeixia0101/zf-novel-writer) <br>
- [README](artifact/README.md) <br>
- [Tools guide](artifact/tools/README.md) <br>
- [Architect agent design](artifact/docs/ARCHITECT_AGENT_DESIGN.md) <br>
- [Orchestrator archive guide](artifact/ORCHESTRATOR_ARCHIVE_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with command examples; generated novel chapters as text files and continuity data as JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create and update project files such as chapter drafts, summaries, plans, and continuity records.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
