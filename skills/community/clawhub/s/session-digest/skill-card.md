## Description:

Session Digest extracts same-day OpenClaw session conversations so an agent can summarize them into a daily memory Markdown file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pazzilivo](https://clawhub.ai/user/pazzilivo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to extract conversations from a selected date and ask an agent to turn them into a compact memory/YYYY-MM-DD.md digest.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read conversation history from every local OpenClaw agent for the selected date.

Mitigation: Install only when broad local session access is intended; prefer a version that lets the user select which agents to include.

Risk: Raw extracted conversations are written to a predictable shared temporary file.

Mitigation: Review and delete temporary output after use; prefer writing to a private 0600 file under the user's OpenClaw directory.

Risk: Extracted conversations may contain sensitive content that should not appear in long-term memory.

Mitigation: Redact sensitive content before summarization and review the generated memory file before retaining it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pazzilivo/skills/session-digest)
- [Publisher Profile](https://clawhub.ai/user/pazzilivo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown digest plus local text extraction output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local OpenClaw session histories for a selected date and writes raw extracted conversations to /tmp/session-digest-YYYY-MM-DD.txt before summarization.]

## Skill Version(s):

4.1.3 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
