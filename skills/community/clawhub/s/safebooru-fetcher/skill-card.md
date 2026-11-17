## Description:

Downloads safe-rated anime images from Safebooru by tag query and saves the resulting files to a local output directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[litousteven](https://clawhub.ai/user/litousteven)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search Safebooru tags, retrieve original image URLs, and download matching images for local workflows. It is suited to download-only image collection where the caller controls any later review, upload, or publishing step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The downloader can make outbound requests based on URLs returned by Safebooru and redirects, and the download path lacks explicit limits.

Mitigation: Run it in an isolated environment, keep requested counts small, constrain the output directory, and pin or audit dependencies before broader use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/litousteven/skills/safebooru-fetcher)
- [Safebooru](https://safebooru.org)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Markdown guidance and command-line text output with local image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes downloaded images to a caller-selected local directory, defaulting to ./downloads.]

## Skill Version(s):

1.0.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
