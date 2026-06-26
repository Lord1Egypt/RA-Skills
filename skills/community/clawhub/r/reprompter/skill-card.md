## Description: <br>
RePrompter transforms rough prompts into structured XML or Markdown prompts, scores prompt quality, and can optionally produce team briefs and per-agent prompts for Claude Code or OpenClaw orchestration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AytuncYildizli](https://clawhub.ai/user/AytuncYildizli) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, engineers, and agent users use RePrompter to turn vague or compound requests into actionable prompts with clear requirements, constraints, output formats, and success criteria. For larger tasks, it can plan multi-agent work and create scoped sub-prompts for team execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repromptception mode can launch multi-agent Claude/OpenClaw runs and generate tmux commands that write outputs under /tmp. <br>
Mitigation: Review generated tmux commands, working directories, and /tmp paths before execution; use single-prompt mode when orchestration is not needed. <br>
Risk: Prompts, team briefs, and agent outputs may include sensitive user or project data written to temporary files. <br>
Mitigation: Avoid putting secrets or sensitive private data into prompts and remove temporary files after use. <br>
Risk: Generated quality scores are self-assessed and may overstate prompt readiness. <br>
Mitigation: Treat scores as directional and review generated requirements, constraints, and success criteria before using the prompt. <br>


## Reference(s): <br>
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) <br>
- [Anthropic Skills Guide](https://claude.com/blog/complete-guide-to-building-skills-for-claude) <br>
- [Team Brief Template](docs/references/team-brief-template.md) <br>
- [Multi-Agent/Swarm Template](docs/references/swarm-template.md) <br>
- [Feature Template](docs/references/feature-template.md) <br>
- [API Template](docs/references/api-template.md) <br>
- [Security Template](docs/references/security-template.md) <br>
- [Testing Template](docs/references/testing-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with XML prompt blocks, quality score tables, optional team briefs, per-agent sub-prompts, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Single mode produces prompts and scores only; Repromptception mode can include tmux orchestration commands and /tmp output paths.] <br>

## Skill Version(s): <br>
7.0.0 (source: frontmatter and changelog, released 2026-02-12) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
