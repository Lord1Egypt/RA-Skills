## Description:

RePrompter turns rough prompts into structured single-agent or multi-agent prompts with quality scoring and optional team orchestration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aytuncyildizli](https://clawhub.ai/user/aytuncyildizli)

### License/Terms of Use:

MIT

## Use Case:

Developers and prompt authors use RePrompter to convert vague task requests into structured prompts, quality scores, team briefs, and scoped sub-prompts for coding or research agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repromptception can spawn multiple agent sessions, write temporary files, read their outputs, retry work, and persist Claude Code team settings.

Mitigation: Review the generated scope before execution, use explicit trigger phrases, and enable team mode only for work where those agent actions are acceptable.

Risk: The README installation command fetches from the main branch, which can change over time.

Mitigation: Install from a pinned release or reviewed commit before use.

Risk: Prompt-improvement output can be wrong or over-scoped if the original request is ambiguous.

Mitigation: Review generated prompts, requirements, constraints, and success criteria before letting an agent modify a project.

## Reference(s):

- [RePrompter ClawHub Page](https://clawhub.ai/aytuncyildizli/skills/reprompter)
- [README](README.md)
- [Testing Scenarios](TESTING.md)
- [API Template](docs/references/api-template.md)
- [Bugfix Template](docs/references/bugfix-template.md)
- [Content Template](docs/references/content-template.md)
- [Documentation Template](docs/references/docs-template.md)
- [Feature Template](docs/references/feature-template.md)
- [Refactor Template](docs/references/refactor-template.md)
- [Research/Analysis Template](docs/references/research-template.md)
- [Security Template](docs/references/security-template.md)
- [Multi-Agent/Swarm Template](docs/references/swarm-template.md)
- [Team Brief Template](docs/references/team-brief-template.md)
- [Testing Template](docs/references/testing-template.md)
- [UI Component Template](docs/references/ui-template.md)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Complete Guide to Building Skills for Claude](https://claude.com/blog/complete-guide-to-building-skills-for-claude)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and XML-style structured prompts, with optional shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single prompt mode generates a polished prompt and quality score; Repromptception mode can generate team briefs, per-agent prompts, and agent output files under /tmp.]

## Skill Version(s):

7.0.0 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
