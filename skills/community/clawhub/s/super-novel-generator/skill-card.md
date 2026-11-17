## Description:

Generates Chinese web-novel prompts, outlines, chapter drafts, and continuity memory files from a user's genre, direction, or keywords.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hxmeie](https://clawhub.ai/user/hxmeie)

### License/Terms of Use:

MIT-0

## Use Case:

External users and writers use this skill to turn Chinese web-novel ideas into structured prompts, serialized outlines, chapter drafts, and continuity notes. It is especially oriented toward xuanhuan, cultivation, urban, rebirth, system-flow, and other web-fiction formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using --clean during initialization can remove existing generated chapters and output markdown in the current workspace.

Mitigation: Use --clean only when intentionally restarting a novel project, and review or back up output/ and .learnings/ before cleanup.

Risk: Generated fiction can drift toward real-person, real-place, political, historical, military, or explicit sexual content that the skill is designed to avoid.

Mitigation: Apply the skill's fictional-name, fictional-setting, and content-boundary checks before accepting or saving generated chapters.

## Reference(s):

- [Antagonist Design Reference](references/antagonist-design.md)
- [Character Arcs Reference](references/character-arcs.md)
- [De-AI Writing Reference](references/de-ai-writing.md)
- [Minimal Examples](references/examples.md)
- [Plot Structures Reference](references/plot-structures.md)
- [Prompt Guide](references/prompt-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown prose, Markdown files, and optional shell commands for workspace initialization]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local output/ and .learnings/ project files when the user requests persistent work.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
