## Description:

Guides an agent through a Chinese article writing pipeline from reference intake to draft generation, human review, preference learning, and multi-platform publishing output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shing19](https://clawhub.ai/user/shing19)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content teams use this skill to transform reference materials into Chinese article drafts, preserve reviewer comments and highlights, learn from manual edits, and prepare platform-specific publishing assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Publish stage may upload local article images to external services such as R2 or WeChat.

Mitigation: Review the target platforms and image assets before approving publishing steps or upload-related skill calls.

Risk: Diff-and-Learn can propose changes to writing-style skills that affect future articles.

Mitigation: Approve style-skill updates only after reviewing the generated diff analysis and confirming the preference changes should persist.

## Reference(s):

- [Diff-and-Learn workflow](references/diff-learn.md)
- [ClawHub skill page](https://clawhub.ai/shing19/skills/writing-pipeline)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files, structured notes, platform-specific article text, image asset instructions, shell commands, and metadata configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update article directories, drafts, final copy, diff analysis, platform output folders, image mappings, and publishing metadata.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
