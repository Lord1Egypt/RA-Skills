## Description:

Re Blog Writer researches a user-provided topic in a browser and writes a complete, human-sounding Markdown blog post saved under ~/blogs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dishant0406](https://clawhub.ai/user/dishant0406)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, marketers, and developers use this skill to turn a topic or angle into a researched 1200-1500 word blog draft with a five-part structure and casual voice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill saves drafts under ~/blogs, and overwrite handling is not described.

Mitigation: Check whether ~/blogs/<subject-slug>.md already exists before saving or reviewing the generated post.

Risk: The skill uses browser research and may include current claims from external sources.

Mitigation: Review sources and factual claims before publishing the generated blog post.

## Reference(s):

- [Human Voice](references/human-voice.md)
- [Research](references/research.md)
- [Structure](references/structure.md)
- [Writing Style](references/writing-style.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown file and completion report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves the finished post to ~/blogs/<subject-slug>.md and reports the subject, file path, word count, sources used, and browser tab closure.]

## Skill Version(s):

1.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
