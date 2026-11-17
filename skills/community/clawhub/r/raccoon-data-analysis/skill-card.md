## Description:

Raccoon Data Analysis helps an agent manage remote Raccoon data-analysis sessions, upload optional user-provided files, stream analysis responses, and download generated artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raccoon-office](https://clawhub.ai/user/raccoon-office)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route file-based or prompt-only data-analysis requests to a configured Raccoon API service and receive streamed results plus downloaded artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Files and credentials may be sent to an unvalidated RACCOON_API_HOST endpoint.

Mitigation: Install only when the Raccoon service is trusted, set RACCOON_API_HOST to a known HTTPS endpoint, and confirm user consent before uploading files.

Risk: Downloaded artifacts may be unsafe or mishandled.

Mitigation: Prefer --no-open for downloaded artifacts, verify the host, download URL, and filename handling, and treat downloaded files as untrusted until reviewed.

Risk: Authentication checks can reveal token fragments.

Mitigation: Avoid sharing auth-check output and keep RACCOON_API_TOKEN out of logs, screenshots, and public transcripts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/raccoon-office/skills/raccoon-data-analysis)
- [Raccoon Homepage](https://xiaohuanxiong.com)
- [API Reference](references/API_REFERENCE.md)
- [API Cheatsheet](references/CHEATSHEET.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown and terminal output with streamed text, optional code excerpts, shell commands, and downloaded artifact file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated artifacts are downloaded to ./raccoon/dataanalysis/ unless download is disabled.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
