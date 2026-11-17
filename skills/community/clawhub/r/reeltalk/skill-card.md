## Description:

Helper for processing shared video links: it takes a URL, downloads the audio track, creates a text transcript, and produces a summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ameshalexk](https://clawhub.ai/user/ameshalexk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use ReelTalk to understand shared video links without watching them by generating a transcript or OCR fallback and a concise plain-English summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs local media tools on remote URLs and the release evidence rates it as review-level.

Mitigation: Use it in a contained workspace and avoid untrusted or attacker-supplied URLs.

Risk: Release evidence identifies risk from unsafe URL handling and broad temporary-file deletion.

Mitigation: Prefer a version with structural URL parsing, per-run temporary directories, and clear trust boundaries for downloaded text.

Risk: The X/Twitter fallback uses an external fxtwitter API call.

Mitigation: Confirm user consent for the fallback and validate returned media URLs before download.

## Reference(s):

- [ReelTalk on ClawHub](https://clawhub.ai/ameshalexk/skills/reeltalk)
- [Amesh Alex Kuruvilla ClawHub profile](https://clawhub.ai/user/ameshalexk)
- [fxtwitter API fallback](https://api.fxtwitter.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summary with transcript or OCR-derived text and inline shell command steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local media tools and may process downloaded media from remote URLs.]

## Skill Version(s):

1.4.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
