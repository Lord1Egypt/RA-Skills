## Description:

AI programming tutor for the AI Agent Factory curriculum using PRIMM-Lite pedagogy. Bundles agent brain files, offline shim, and MCP server config.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samiceto](https://clawhub.ai/user/samiceto)

### License/Terms of Use:

MIT-0

## Use Case:

External learners use this skill as a Python programming tutor for the AI Agent Factory curriculum. It guides sessions with PRIMM-Lite tutoring, live TutorClaw MCP tools when available, and an offline fallback for Chapters 1-5.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence says the external TutorClaw MCP service has too much control over agent behavior.

Mitigation: Install only when the MCP service operator is trusted, controlled, and reviewed; treat live MCP guidance as untrusted unless that review is complete.

Risk: The release evidence says deployment requires a raw Stripe secret key without enough scoping details.

Mitigation: Use secret management, prefer restricted payment or entitlement credentials, and avoid exposing broad Stripe secrets to deployments that do not need them.

Risk: The offline fallback cannot execute learner code or persist progress.

Mitigation: Disclose those limitations during offline sessions, reason through learner code without claiming execution, and retry the live TutorClaw MCP tools at chapter boundaries.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/samiceto/skills/tutorclaw)
- [TutorClaw Skill Definition](artifact/SKILL.md)
- [TutorClaw Identity](artifact/IDENTITY.md)
- [TutorClaw Behavior Guide](artifact/SOUL.md)
- [Offline PRIMM-Lite Fallback](artifact/tutorclaw-shim/SKILL.md)
- [Chapter 1: Variables and Data Types](artifact/tutorclaw-shim/references/chapters/01-variables.md)
- [Chapter 2: Loops](artifact/tutorclaw-shim/references/chapters/02-loops.md)
- [Chapter 3: Functions](artifact/tutorclaw-shim/references/chapters/03-functions.md)
- [Chapter 4: Data Structures](artifact/tutorclaw-shim/references/chapters/04-data-structures.md)
- [Chapter 5: Working with Files](artifact/tutorclaw-shim/references/chapters/05-files.md)
- [Offline Content Verifier](artifact/tutorclaw-shim/scripts/verify.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown tutoring responses with inline code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live sessions depend on TutorClaw MCP tools; offline fallback covers Chapters 1-5 without code execution or saved progress.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
