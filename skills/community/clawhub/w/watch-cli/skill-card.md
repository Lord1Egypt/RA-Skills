## Description:

Watch any social video -> get an architecture diagram, working component, runnable notebook, or step-by-step cheat sheet - automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sonpiaz](https://clawhub.ai/user/sonpiaz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a user provides a social video URL and wants the content summarized, explained, implemented, converted into an architecture diagram, or turned into a runnable notebook or cheat sheet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback installer runs a downloaded shell script before local verification.

Mitigation: Prefer the Homebrew install path or independently inspect and verify the release installer before use.

Risk: Using the skill fetches video URLs and can upload extracted audio to Kyma API for transcription.

Mitigation: Use it only for videos the user is comfortable processing this way, or install local transcription when uploads are not acceptable.

Risk: Browser-cookie access can expose local browser session data to the target video platform.

Mitigation: Enable browser-cookie access only after explicit user consent and only for videos that require authenticated access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sonpiaz/skills/watch-cli)
- [watch-cli homepage](https://github.com/sonpiaz/watch-cli)
- [Prompt templates](https://github.com/sonpiaz/watch-cli/tree/main/prompts)
- [Output schema](https://github.com/sonpiaz/watch-cli/blob/main/docs/output-schema.md)
- [Exit codes](https://github.com/sonpiaz/watch-cli/blob/main/docs/exit-codes.md)
- [Archive documentation](https://github.com/sonpiaz/watch-cli/blob/main/docs/archive.md)
- [Pinned release installer](https://github.com/sonpiaz/watch-cli/releases/download/v0.3.4/install.sh)
- [Kyma API](https://kymaapi.com/?src=skill:watch)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code blocks and generated artifacts; the watch CLI can emit JSON or labeled text for agent parsing.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use video frames, transcripts, timestamps, and cached archive records as source material.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
