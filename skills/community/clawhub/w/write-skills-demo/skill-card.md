## Description: <br>
Use when creating new skills, editing existing skills, or verifying skills work before deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freshman94](https://clawhub.ai/user/freshman94) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this documentation-only skill to create, edit, and pressure-test agent skills with TDD-style scenarios before deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or revised SKILL.md and CLAUDE.md content could encode incorrect or misleading guidance. <br>
Mitigation: Review generated documentation before making it persistent, then test it with synthetic scenarios before deployment. <br>
Risk: Pressure-test scenarios can accidentally include private or sensitive operational details. <br>
Mitigation: Keep examples and test scenarios synthetic, and avoid secrets, credentials, private data, or real incident details. <br>


## Reference(s): <br>
- [Skill release page](https://clawhub.ai/freshman94/write-skills-demo) <br>
- [Anthropic best practices](anthropic-best-practices.md) <br>
- [Testing skills with subagents](testing-skills-with-subagents.md) <br>
- [Persuasion principles](persuasion-principles.md) <br>
- [CLAUDE.md testing example](examples/CLAUDE_MD_TESTING.md) <br>
- [Claude context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with checklists, tables, scenario prompts, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; no executable code is bundled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
