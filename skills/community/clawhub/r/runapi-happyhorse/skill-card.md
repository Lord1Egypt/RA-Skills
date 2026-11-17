## Description:

HappyHorse helps agents generate video clips through RunAPI from text, image inputs, ordered reference images, or source video edits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route one-off HappyHorse media generation through the RunAPI CLI, or to integrate HappyHorse into applications through SDKs. The skill emphasizes contract discovery, request validation, task tracking, and deliverable verification before reporting completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned third-party RunAPI CLI from a custom Homebrew tap.

Mitigation: Review the CLI source and provenance before installation, and prefer a pinned, verified CLI version when available.

Risk: The workflow uses RunAPI credentials and may upload local media to the service.

Mitigation: Provide only credentials and local media intended for RunAPI processing, and prefer environment or saved CLI authentication over interactive login.

Risk: Generated media downloads may be unexpected, empty, or mismatched to the requested output type.

Mitigation: Download outputs into a controlled directory and validate that each file is non-empty and matches the expected MIME type before opening or reporting completion.

## Reference(s):

- [HappyHorse model overview](https://runapi.ai/models/happyhorse.md)
- [RunAPI Alibaba provider overview](https://runapi.ai/providers/alibaba.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [HappyHorse SDK integration](https://github.com/runapi-ai/happyhorse-sdk)
- [HappyHorse homepage](https://runapi.ai/models/happyhorse)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON file examples, and integration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce request and task JSON, downloaded media files, and SDK integration code depending on the user's goal.]

## Skill Version(s):

0.2.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
