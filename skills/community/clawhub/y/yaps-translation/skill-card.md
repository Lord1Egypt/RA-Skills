## Description:

Translate text, Markdown, or subtitle files with a local Yaps installation while preserving source files and subtitle timing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaps](https://clawhub.ai/user/yaps)

### License/Terms of Use:

MIT

## Use Case:

Individuals and teams use this skill to translate short text or text, Markdown, and SRT files with Yaps, retaining originals and checking subtitle timing and document structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local Yaps integration can expose commands beyond translation and inspect installation or account status.

Mitigation: Review requested commands and authorize only translation-related actions; decline unexpected account, Keychain, checkout, or broad file requests.

Risk: Translation models may require downloads and Yaps may retain project or media-derived state.

Mitigation: Confirm download size and obtain approval before enabling models; review retained Yaps projects and avoid submitting sensitive content without authorization.

## Reference(s):

- [Yaps Translation on ClawHub](https://clawhub.ai/yaps/skills/yaps-translation)
- [Yaps download](https://yaps.ai/download)
- [Yaps local runtime guide](references/runtime.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Subtitle files, Guidance]

**Output Format:** [Plain text, Markdown, or SRT, with a brief result summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves source files; checks subtitle cue indices and timestamps when translating SRT.]

## Skill Version(s):

1.0.2 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
