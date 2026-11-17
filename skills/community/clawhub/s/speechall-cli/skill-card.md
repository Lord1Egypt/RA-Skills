## Description:

Install and use the Speechall CLI for speech-to-text transcription of audio and video files, model discovery, diarization, subtitles, and terminal-based provider workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atacan](https://clawhub.ai/user/atacan)

### License/Terms of Use:


## Use Case:

Developers, engineers, and terminal users use this skill to install and operate the Speechall CLI for transcribing local audio or video files, listing speech-to-text models, and selecting transcription features such as diarization, subtitles, language, and provider model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to install an unpinned third-party executable.

Mitigation: Prefer a pinned release with verified checksums or signatures, and install it in a user-scoped location.

Risk: Transcription can send confidential, personal, regulated, or consent-sensitive recordings to external services.

Mitigation: Review Speechall and provider data-handling terms before use, and avoid submitting sensitive media without appropriate authorization.

Risk: Passing the Speechall API key on the command line can expose credentials through shell history or process listings.

Mitigation: Provide the API key with the SPEECHALL_API_KEY environment variable when possible.

## Reference(s):

- [Speechall CLI GitHub releases](https://github.com/Speechall/speechall-cli/releases)
- [Speechall API key creation page](https://speechall.com/console/api-keys)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CLI options, environment variable setup, provider/model selection guidance, and stdout redirection examples.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
