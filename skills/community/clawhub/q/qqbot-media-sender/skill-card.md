## Description:

One-click QQ media tag generation for images, videos, and files, with batch processing and file-size checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bg1avd](https://clawhub.ai/user/bg1avd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to prepare QQBot-compatible media tags and command-line output for local image, video, and document paths. Users should verify the produced tags before using them in any QQBot runtime.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may expose unintended local files because it emits absolute local paths inside raw QQ media tags.

Mitigation: Run it only on explicitly selected files from non-sensitive directories, and review generated tags before passing them to any QQBot runtime.

Risk: The documented group delivery, compression, and max-size controls are not reliably evidenced by the implementation.

Mitigation: Do not depend on these options for access control, delivery routing, or file handling until the behavior is reviewed and tested.

Risk: The package appears to prepare or print tags rather than send media through a scoped QQ API.

Mitigation: Treat output as generated text for a separate QQBot runtime, not as proof that files were delivered.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bg1avd/skills/qqbot-media-sender)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Console text with QQ media tags and command-line status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local absolute file paths inside QQ media tags; no scoped QQ API call is evidenced.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
