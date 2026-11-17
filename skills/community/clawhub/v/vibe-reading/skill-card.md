## Description:

Intelligent book reading and analysis skill that turns user-provided EPUB or TXT books into chapter splits, deep English summaries, and an interactive HTML reader.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drbillwang](https://clawhub.ai/user/drbillwang)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to process long EPUB or TXT books into cleaned text, chapter files, high-fidelity Markdown summaries, and a static HTML reading interface. It is intended for book analysis workflows where the agent reads sequentially and preserves contextual continuity across chapters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates local derived files that may contain sensitive book content.

Mitigation: Review or delete generated input/, chapters/, summaries/, and html/ directories after use, especially for sensitive books.

Risk: Python packages and the HTML Markdown renderer are not pinned or bundled in the release evidence.

Mitigation: Prefer pinned Python dependencies and a bundled local Markdown renderer before deployment in controlled environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/drbillwang/skills/vibe-reading)
- [Project homepage](https://github.com/drbillwang/vibe-reading-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, generated local text files, generated Python scripts, and a static HTML reader]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local input/, chapters/, summaries/, and html/ directories; the HTML reader is static and does not embed API keys or AI service calls.]

## Skill Version(s):

2.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
