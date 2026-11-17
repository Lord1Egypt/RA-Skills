## Description:

Advanced thinking model that improves decision-making speed and accuracy. Integrates with memory system to compare and integrate previous thinking models for continuous enhancement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xqicxx](https://clawhub.ai/user/xqicxx)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to apply a structured decision-making framework that selects thinking modes, compares prior approaches from memory, and produces recommendations or conclusions with documented confidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change agent reasoning style when invoked, which may introduce overconfident or misleading decision guidance.

Mitigation: Review outputs before acting on them, narrow use to appropriate decision-analysis tasks, and revise broad system-prompt language before deployment.

Risk: The skill writes local plaintext thinking history and configuration under ~/.claude/thinking_models.

Mitigation: Avoid using the skill with secrets, credentials, private business details, medical/legal/financial matters, or shared machines unless persistence is disabled or reviewed.

Risk: Automatic memory behavior may retain more task context than users expect.

Mitigation: Make memory opt-in, document stored fields and retention, and provide clear deletion, recovery, and permission controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xqicxx/skills/thinking-model-enhancer)
- [Publisher profile](https://clawhub.ai/user/xqicxx)
- [README](artifact/README.md)
- [CHANGELOG](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include structured decision analysis, selected thinking mode, confidence notes, performance metrics, and memory-informed recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact changelog, released 2026-01-31)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
