## Description:

Design, test, review, and maintain agent skills for OpenClaw systems using multi-agent iterative refinement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chunhualiao](https://clawhub.ai/user/chunhualiao)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent-kit maintainers use this skill to create, review, test, refactor, and maintain OpenClaw agent skills with structured quality gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad private memory search can surface prior-session context that is not needed for a task.

Mitigation: Use memory search only when prior-session context is explicitly needed, and run the skill in a dedicated workspace.

Risk: The workflow depends on external DeepWiki behavior that may drift or be unavailable.

Mitigation: Verify the installed DeepWiki dependency before using the skill and confirm OpenClaw API behavior against current source.

Risk: Scheduled follow-up jobs can continue workflow actions after the immediate user interaction.

Mitigation: Enable cron-style follow-ups only after reviewing the exact purpose and workspace scope.

Risk: Git commits or remote pushes can publish unintended changes.

Mitigation: Review the exact diff and destination before allowing commits or pushes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chunhualiao/skills/skill-engineer)
- [References](references/README.md)
- [Designer Guide](references/designer-guide.md)
- [Reviewer Rubric](references/reviewer-rubric.md)
- [Tester Protocol](references/tester-protocol.md)
- [Validation Scripts](scripts/README.md)
- [Functional Tests](tests/functional-tests.md)
- [Anthropic Complete Guide to Building Skills for Claude](https://claude.com/blog/complete-guide-to-building-skills-for-claude)
- [Anthropic Complete Guide PDF](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf?hsLang=en)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code, shell command, and configuration snippets; may produce or update skill artifact files when run in a writable workspace.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are quality-gated through reviewer and tester workflows before release actions.]

## Skill Version(s):

3.2.0 (source: server release metadata and skill.yml; SKILL.md frontmatter lists 3.6.0 and CHANGELOG top entry lists 3.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
