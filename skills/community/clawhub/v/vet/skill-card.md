## Description:

Run vet immediately after ANY logical unit of code changes. Do not batch your changes, do not wait to be asked to run vet, make sure you are proactive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrewlaack-collab](https://clawhub.ai/user/andrewlaack-collab)

### License/Terms of Use:


## Use Case:

Developers and coding agents use vet after small code changes to review git diffs and, when explicitly configured, conversation history for issues that tests or ordinary review may miss. It supports frequent code-review checks across Codex, Claude Code, and OpenCode workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send git diffs and full coding-session history, including prompts, code snippets, file paths, command output, and tool results, into another review process.

Mitigation: Use vet without conversation history for sensitive repositories unless the user explicitly approves sharing that session context.

Risk: Session discovery can select the wrong local conversation when titles, timestamps, or search strings are ambiguous.

Mitigation: Verify the selected session against the current conversation before passing it to a history loader.

Risk: The CLI package and skill scripts may become outdated as agent harness formats change.

Mitigation: Pin and verify the verify-everything package and update the CLI and skill files from trusted sources when compatibility issues appear.

## Reference(s):

- [ClawHub vet skill page](https://clawhub.ai/andrewlaack-collab/skills/vet)
- [vet repository](https://github.com/imbue-ai/vet)
- [vet skill source](https://github.com/imbue-ai/vet/tree/main/skills/vet)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, markdown]

**Output Format:** [Markdown with inline shell commands and command output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can run without conversation history; optional history loaders export local coding-session messages and tool activity for review.]

## Skill Version(s):

0.2.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
