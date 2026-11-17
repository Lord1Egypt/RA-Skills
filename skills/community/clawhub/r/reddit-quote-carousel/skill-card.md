## Description:

Create an Instagram carousel from a popular-picks list with Reddit quotes, including a clean cover slide and quote-style attraction slides.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyduckler](https://clawhub.ai/user/psyduckler)

### License/Terms of Use:


## Use Case:

Content creators and social media operators use this skill to turn tabiji.ai popular-picks pages into Instagram carousel posts with destination photos, Reddit quotes, captions, and publishing steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can publish content publicly to Instagram.

Mitigation: Require explicit manual confirmation before uploading, creating carousel containers, or publishing a post.

Risk: The workflow temporarily hosts generated images in the tabiji repository.

Mitigation: Use the skill only when temporary repository hosting is intended, and verify cleanup of hosted images and local temporary files after publishing.

Risk: Shell commands may include web-sourced text such as quotes, attraction names, and slugs.

Mitigation: Pass dynamic values through safe subprocess argument arrays, or strictly validate and escape web-sourced text before command execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/psyduckler/skills/reddit-quote-carousel)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, API calls]

**Output Format:** [Markdown guidance with JSON manifest examples, shell command examples, image file outputs, caption text, and publishing workflow steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local carousel slide images and may publish a carousel post after user review and confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
