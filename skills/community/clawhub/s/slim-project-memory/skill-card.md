## Description:

Restructures or initializes a compact project memory system with a router-style CLAUDE.md, a gitignored local environment reference, topical docs, and a housekeeping protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adelvillar1](https://clawhub.ai/user/adelvillar1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to reduce project-memory bloat, preserve environment context safely, and organize persistent agent documentation into a maintainable docs tree.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence warns that contradictory credential-handling instructions could cause real secrets to be persisted in a local agent memory file.

Mitigation: Keep only environment variable names, non-secret service names, and non-secret URLs in CLAUDE.local.md; store secret values in environment managers or ignored .env files.

Risk: The skill can guide agents through DB migrations, commits, pushes, and other high-impact project operations.

Mitigation: Require explicit approval in the current turn before migrations, commits, pushes, destructive commands, or operations against non-local environments.

Risk: The security guidance notes that unpinned npx commands may introduce avoidable supply-chain risk.

Mitigation: Prefer pinned local project dependencies or explicitly pinned package versions when running generated shell commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adelvillar1/skills/slim-project-memory)
- [CLAUDE template](references/CLAUDE-template.md)
- [Local environment reference template](references/CLAUDE-local-template.md)
- [Housekeeping protocol](references/housekeeping-protocol.md)
- [Cruise Intelligence migration case study](references/cruise-intelligence-case-study.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or edits project documentation files and local configuration references; user review is required before commits, pushes, migrations, or secret-related changes.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
