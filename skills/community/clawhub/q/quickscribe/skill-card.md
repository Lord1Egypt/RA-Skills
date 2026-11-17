## Description:

Quickscribe transcribes local videos or public video URLs through the GuaiKei cloud service and can use prompts to produce cleaned transcripts, summaries, rewrites, quotes, shot outlines, translations, or meeting notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to convert a single video file or public URL into usable text, then optionally transform that content into summaries, social copy, scripts, translations, or structured notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected local videos, downloaded URL content, prompts, task IDs, the API token, and some file metadata are sent to a third-party service.

Mitigation: Use only with content approved for third-party GuaiKei processing; avoid confidential, regulated, or policy-restricted media unless separate review permits it.

Risk: Arbitrary URL input can download and upload unexpected internal, localhost, metadata-service, untrusted, or oversized content.

Mitigation: Constrain execution with URL allowlists, private-address blocking, media validation, and size limits before using URL inputs.

Risk: Transcription and prompt-generated outputs can be inaccurate for noisy audio, overlapping speakers, accents, or high-stakes domains.

Mitigation: Require human review before relying on outputs for legal, medical, financial, compliance, or other sensitive decisions.

## Reference(s):

- [Quickscribe ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/quickscribe)
- [GuaiKei Service Site](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or prompt-shaped Markdown on stdout, with progress and diagnostics on stderr.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; accepts one local file, public URL, or previous task ID plus an optional prompt.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
