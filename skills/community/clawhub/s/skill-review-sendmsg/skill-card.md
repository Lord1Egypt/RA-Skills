## Description:

Performs structured repository code reviews with local checks, hard-rule blocking, LLM batch review, and optional Telegram notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dexing2635-tech](https://clawhub.ai/user/dexing2635-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release operators use this skill to review repository changes before merge or deployment, focusing on actionable correctness, safety, test coverage, and maintainability findings. The helper scripts target PHP, JavaScript, TypeScript, SQL, and shell diffs rather than Python files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository diffs, review metadata, or logs may be sent to configured external LLM and Telegram services.

Mitigation: Use only with repositories where that data sharing is approved, and review provider, token, and notification configuration before installation.

Risk: The skill advertises Python review, but the helper scripts filter for PHP, JavaScript, TypeScript, SQL, and shell files.

Mitigation: Do not rely on this release for Python review unless the target-file filtering and documentation are corrected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dexing2635-tech/skills/skill-review-sendmsg)
- [Reference README](references/README.md)
- [Original Skill Definition](references/SKILL.original.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown review findings and JSON helper-script results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include verdicts, file and line references, local check failures, LLM review findings, suggested fixes, and configured notification or log summaries.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
