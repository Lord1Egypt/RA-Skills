## Description: <br>
Build high-quality Agent Skills for Claude following official Anthropic best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tenequm](https://clawhub.ai/user/tenequm) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and skill authors use this skill to create, review, troubleshoot, and publish Agent Skills with clearer structure, descriptions, progressive disclosure, tests, and distribution guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger language can activate the skill for general skill-building requests where only a narrower answer is needed. <br>
Mitigation: Use it as reference guidance and confirm the requested target surface before applying surface-specific recommendations. <br>
Risk: Server-displayed capability tags may overstate runtime risk because the docs mention payments, tokens, credentials, and transactions as examples. <br>
Mitigation: Treat the submitted artifact as documentation-only and review any generated skill or command separately before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tenequm/skills-best-practices) <br>
- [Homepage](https://github.com/tenequm/skills/tree/main/skills/skills-best-practices) <br>
- [Agent Skills Spec](https://agentskills.io/specification) <br>
- [Claude Code Skills Docs](https://code.claude.com/docs/en/skills) <br>
- [API Skills Guide](https://platform.claude.com/docs/en/build-with-claude/skills-guide) <br>
- [Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) <br>
- [Anthropic Skills Repo](https://github.com/anthropics/skills) <br>
- [Description writing guide](references/description-guide.md) <br>
- [Patterns and workflows](references/patterns.md) <br>
- [Claude Code features](references/claude-code-features.md) <br>
- [Quality checklist](references/checklist.md) <br>
- [ClawHub publishing](references/clawhub-publishing.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with examples, YAML frontmatter snippets, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; no executable scripts are included in the submitted artifact.] <br>

## Skill Version(s): <br>
0.5.0 (source: evidence.json release version, SKILL.md metadata, and CHANGELOG.md released 2026-06-05) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
