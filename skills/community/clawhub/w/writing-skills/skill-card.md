## Description: <br>
Guides agents through creating, editing, and testing reusable skills with a test-driven documentation workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlc000190](https://clawhub.ai/user/zlc000190) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to create or revise skills and verify they work before deployment. It is suited to reusable process documentation, skill authoring, and skill testing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or edited skill files can steer future agent behavior in unintended ways. <br>
Mitigation: Review any generated or edited skill files before keeping or deploying them, and scan the skill before release. <br>
Risk: Pressure-testing prompts can encourage unrealistic or risky behavior if run outside a controlled evaluation context. <br>
Mitigation: Keep skill pressure tests confined to controlled subagent or test environments. <br>
Risk: The optional diagram helper runs Graphviz over skill content and writes generated files. <br>
Mitigation: Run the helper only on trusted skill directories with a trusted Graphviz installation. <br>


## Reference(s): <br>
- [Anthropic Skill Authoring Best Practices](anthropic-best-practices.md) <br>
- [Testing Skills with Subagents](testing-skills-with-subagents.md) <br>
- [Persuasion Principles](persuasion-principles.md) <br>
- [Claude Context Windows](https://platform.claude.com/docs/en/build-with-claude/context-windows) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional code blocks, shell commands, and diagram rendering outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The optional Graphviz helper can render dot diagrams from a skill file into SVG files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
