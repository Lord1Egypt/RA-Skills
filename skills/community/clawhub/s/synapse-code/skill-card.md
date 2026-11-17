## Description:

Synapse Code is an intelligent development workflow skill that initializes projects, runs multi-agent pipelines, captures project knowledge, and supports impact analysis across code, writing, design, analytics, translation, and research tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ankechenlab-node](https://clawhub.ai/user/ankechenlab-node)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project teams use Synapse Code to route software development and knowledge-work requests through standalone, lite, full, or parallel workflows. It helps generate code, Markdown deliverables, shell commands, configuration guidance, status checks, memory records, and impact-analysis guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs mutable npm code as part of normal setup.

Mitigation: Review before installing, run the installer with --dry-run first, and use --skip-npm when the npm dependency is not required.

Risk: The skill writes persistent project memory and the security evidence notes insufficient path validation.

Mitigation: Inspect config.json paths before running workflows and restrict use to trusted project directories.

Risk: Pipeline summary files influence auto-log behavior.

Mitigation: Only use trusted pipeline_summary.json files and review generated memory entries before relying on them.

Risk: Cleanup or overwrite operations can be broad if run without review.

Mitigation: Avoid running cleanup or forced install commands blindly; preview actions and review target paths first.

## Reference(s):

- [Synapse Code GitHub homepage](https://github.com/ankechenlab-node/synapse-code)
- [README](artifact/README.md)
- [Agent Guide](artifact/AGENT_GUIDE.md)
- [Pipeline Architecture](artifact/PIPELINE_ARCHITECTURE.md)
- [Production Scenarios](artifact/PRODUCTION_SCENARIOS.md)
- [Troubleshooting](artifact/TROUBLESHOOTING.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, code snippets, shell commands, JSON configuration, and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update project memory files and pipeline summaries when configured.]

## Skill Version(s):

2.0.1 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
