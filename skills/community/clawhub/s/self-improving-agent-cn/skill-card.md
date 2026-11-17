## Description:

Self Improving Agent CN helps agents record command errors, user corrections, and best practices as reusable long-term memory for future work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhengxinjipai](https://clawhub.ai/user/zhengxinjipai)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to capture command failures, corrections, and best-practice notes as reusable long-term memory. Agents can check that memory before future actions to reduce repeated mistakes and preserve project preferences across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic memory writes can persist user text, command failures, and suggested fixes into future agent behavior.

Mitigation: Review memory entries before reuse, periodically remove stale entries, and require explicit review before saving sensitive text, raw command lines, or sudo-based fixes.

Risk: Persisted corrections and best practices can change later sessions without enough user control.

Mitigation: Keep user-visible memory files available for inspection and make deletion or correction part of the normal review workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhengxinjipai/skills/self-improving-agent-cn)
- [Publisher profile](https://clawhub.ai/user/zhengxinjipai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; JSONL memory records when helper scripts are used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local memory records and update project memory or instruction files when the agent follows the skill guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
