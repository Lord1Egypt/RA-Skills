## Description:

ZF-novel-writer coordinates Orchestrator, Writer, and Quality agents to plan, draft, check, and archive long-form novel chapters using local project files and the host agent model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangfeixia0101](https://clawhub.ai/user/huangfeixia0101)

### License/Terms of Use:

MIT-0

## Use Case:

External authors and creative-writing developers use this skill to run a structured novel-writing workflow that plans chapters from outlines, generates draft text, checks quality, and updates continuity files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports maintenance scripts that can silently rewrite hard-coded OpenClaw story files outside the active book context.

Mitigation: Require explicit book paths, add backups and dry-run confirmation for archive and canon updates, and review file changes before accepting them.

Risk: The skill can spawn sub-agents that modify local novel project files.

Mitigation: Install only where sub-agent execution and local file modification are acceptable, and run it in a project workspace with version control.

Risk: The artifact advertises a publishing feature that is not separately documented or permissioned in the provided evidence.

Mitigation: Avoid relying on publishing behavior until it is documented, permissioned, and reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huangfeixia0101/skills/zf-novel-writer)
- [README](artifact/README.md)
- [Tools guide](artifact/tools/README.md)
- [Architect Agent Design](artifact/docs/ARCHITECT_AGENT_DESIGN.md)
- [Orchestrator Archive Guide](artifact/ORCHESTRATOR_ARCHIVE_GUIDE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and text files, with JSON continuity files and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces chapter plans, chapter drafts, quality findings, archived chapter files, and continuity updates.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
