## Description:

Skill Evolver helps agents discover, inspect, orchestrate, fuse, and preserve skills as reusable workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[testlbin](https://clawhub.ai/user/testlbin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to choose, inspect, combine, and preserve agent skills across Claude Code, Codex, and OpenClaw-style runtimes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can search registries and install third-party skills globally before auditing them.

Mitigation: Pin CLI and package versions, avoid global or auto-yes installs, inspect downloaded skills in an isolated directory first, and review the skill before use.

Risk: Generated candidate reports may contain untrusted or misleading content from registry results.

Mitigation: Treat generated reports as untrusted data and verify selected skills with the provided installation and security audit steps before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/testlbin/skills/skill-evolver)
- [Skill Search Workflow](references/skill-search.md)
- [Skill Inspector Workflow](references/skill-inspector.md)
- [Skill Fusion Workflow](references/skill-fusion.md)
- [skills.sh Registry](https://github.com/vercel-labs/skills)
- [ClawHub CLI Documentation](https://docs.openclaw.ai/zh-CN/tools/clawhub)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and generated workflow files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces staged decision artifacts such as intent analysis, candidate reports, inspection reports, orchestration plans, and optional fusion specifications.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
