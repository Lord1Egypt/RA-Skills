## Description:

Generates a 1600-pixel-wide WebP blog thumbnail from a supplied topic using the user's configured pixr CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dishant0406](https://clawhub.ai/user/dishant0406)

### License/Terms of Use:

MIT-0

## Use Case:

Blog authors and content teams use this skill to create topic-based thumbnails and link the resulting image to a matching blog metadata record when one exists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sourcing ~/.zshrc may execute shell-profile commands and expose configured credentials to pixr.

Mitigation: Review the shell profile and confirm credential use before sourcing it.

Risk: Installing pixr-cli globally changes the user's environment.

Mitigation: Ask for approval before a global npm installation.

Risk: Generated files and automatic blog metadata edits can change local content unexpectedly.

Mitigation: Confirm output and metadata targets before writing, and review the matching JSON update.

## Reference(s):

- [ClawHub blog-image release](https://clawhub.ai/dishant0406/skills/re-blog-image)
- [Image Generation Reference](references/image-generation.md)

## Skill Output:

**Output Type(s):** [Image files, Shell commands, Status report]

**Output Format:** [WebP image and text completion report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates one 1600-pixel-wide thumbnail under ~/blog-images by default; may update the thumbnail_path in matching ~/blog-meta JSON.]

## Skill Version(s):

1.1.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
