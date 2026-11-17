## Description:

Openclaw analyzes EPUB or TXT books by splitting them into chapters, producing Chinese chapter summaries, and generating an interactive static HTML reader.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drbillwang](https://clawhub.ai/user/drbillwang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to process long EPUB or TXT books into structured chapter files, high-detail Chinese Markdown summaries, and a static interactive reader for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install unpinned Python packages while processing EPUB files, which can change the Python environment.

Mitigation: Run it in a sandbox and preinstall reviewed, pinned dependencies before use.

Risk: The generated HTML reader loads third-party JavaScript from a CDN.

Mitigation: Replace the CDN script with a reviewed local pinned copy before opening generated readers with network access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/drbillwang/skills/vibe-reading-cn)
- [Project homepage](https://github.com/drbillwang/vibe-reading-skill-CN)
- [Publisher profile](https://clawhub.ai/user/drbillwang)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown summaries, JSON chapter lists, text files, and static HTML]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Simplified Chinese analysis and may create input, chapters, summaries, and html directories.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
