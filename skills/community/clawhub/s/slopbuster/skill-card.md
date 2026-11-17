## Description:

Slopbuster helps agents strip AI patterns from prose, code, and academic writing using rule-based diagnosis, two-pass revision, scoring, and voice guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, developers, and researchers use Slopbuster through an agent to diagnose and rewrite AI-patterned prose, code comments, naming, commits, docstrings, and academic text while preserving meaning and surfacing manual review flags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated rewrites may change meaning, tone, citations, or technical nuance in user-provided prose, code comments, commit messages, or academic text.

Mitigation: Invoke the skill on specific files or text, review diffs before accepting changes, and keep manual review flags in the workflow.

Risk: Optional global agent instructions can affect all future agent writing in a workspace or account.

Mitigation: Add global instructions only when that behavior is intended; otherwise use project-level configuration or explicit invocations.

Risk: Heuristic scoring and pattern checks can overstate or miss AI-like writing signals.

Mitigation: Treat scores as editorial guidance rather than authorship proof, and verify important claims, citations, and disciplinary conventions manually.

Risk: Installation through an external Skills CLI may be unsuitable for security-sensitive environments without verification.

Mitigation: Install manually or pin and verify the Skills CLI before use in security-sensitive environments.

## Reference(s):

- [Slopbuster on ClawHub](https://clawhub.ai/lanyasheng/skills/slopbuster)
- [Setup guide](docs/setup-guide.md)
- [Scoring system](scoring.md)
- [Voice and soul guide](guides/voice-and-soul.md)
- [Style template](guides/style-template.md)
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with rewritten text or code snippets, scores, changelogs, and manual review flags]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write edited files when the user asks the agent to apply rewrites.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact frontmatter, and changelog released 2026-03-24)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
