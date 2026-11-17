## Description:

Search inside videos, generate summaries, and analyze video content using TwelveLabs video understanding AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[james-le-twelve-labs](https://clawhub.ai/user/james-le-twelve-labs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to set up the TwelveLabs Python SDK, index video assets, search by text, transcription, image, or entity reference, and generate video summaries, chapters, highlights, embeddings, and other analyses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides users to upload videos and images to TwelveLabs indexes and assets, which may expose sensitive media to a third-party service.

Mitigation: Only upload videos or images the user is comfortable sending to TwelveLabs and storing in their TwelveLabs account indexes and assets.

Risk: The skill instructs users to install the TwelveLabs Python SDK, introducing normal third-party dependency risk.

Mitigation: Install the SDK in an isolated Python environment and consider pinning the twelvelabs package to a reviewed version.

## Reference(s):

- [TwelveLabs Documentation](https://docs.twelvelabs.io)
- [TwelveLabs API Reference](https://docs.twelvelabs.io/reference)
- [TwelveLabs Python SDK](https://github.com/twelvelabs-io/twelvelabs-python)
- [TwelveLabs Homepage](https://twelvelabs.io)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a TWELVE_LABS_API_KEY and user-selected video assets, indexes, queries, and prompts.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
