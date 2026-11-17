## Description:

Publish WeChat Official Account draft articles through a packaged CLI executable that wraps WeChat API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mesus](https://clawhub.ai/user/mesus)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to create WeChat Official Account draft articles from local article content and images through the fixed getAuth, upload image, upload cover, and addDraft flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install and execute a remote CLI binary from a GitHub Release or direct URL.

Mitigation: Prefer a manually installed, pinned, checksum-verified CLI path and avoid auto-download URLs unless the exact source is trusted.

Risk: WeChat access tokens and GitHub credentials may be exposed through command output, logs, or process metadata.

Mitigation: Unset GITHUB_TOKEN unless required, avoid sharing stdout or stderr, and treat the wrapper's JSON output as sensitive.

## Reference(s):

- [CLI Contract](references/cli-contract.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands; the wrapper produces JSON on stdout and JSON errors on stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local WeChat credentials and prepared content and image files; may call a configured local or downloaded CLI executable.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
