## Description:

Prepare, validate, and explicitly upload YouTube Shorts through the official YouTube Data API with dry-run safety.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidmosiah](https://clawhub.ai/user/davidmosiah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to install and configure YouTube Shorts Agent, check OAuth and privacy readiness, and perform dry-run or explicitly confirmed uploads for user-owned YouTube Shorts workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow can run an unpinned npm package that may change after review.

Mitigation: Review the npm package source, pin an exact package version before installation, and keep dry-run or confirmation steps enabled before any live upload.

Risk: The skill may interact with YouTube credentials, local token files, user media, and upload operations.

Mitigation: Run it with only the files, environment variables, and YouTube credentials needed, and do not print OAuth tokens, API keys, service-account JSON, local token files, or private user data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/davidmosiah/skills/youtube-shorts-agent)
- [YouTube Shorts Agent Repository](https://github.com/davidmosiah/youtube-shorts-agent)
- [YouTube Shorts Agent npm Package](https://www.npmjs.com/package/youtube-shorts-agent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance emphasizes dry-run checks, privacy boundaries, and explicit user confirmation before live uploads.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
