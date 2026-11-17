## Description:

Yinxiang Skill lets compatible AI assistants connect to Yinxiang/Evernote so users can create, search, update, organize, and clip notes after authorization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinxiang-team](https://clawhub.ai/user/yinxiang-team)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an AI assistant operate a Yinxiang/Evernote account with user authorization. It supports saving Markdown notes, clipping URLs, searching and listing notes, viewing note details, moving notes, and managing notebooks and tags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read note details and create or modify notes, notebooks, and tags using the user's token.

Mitigation: Install only if the publisher and requested operations are trusted, and confirm note IDs, content replacements, batch moves, and tag changes before execution.

Risk: Credential-handling weaknesses could expose a long-lived Yinxiang token in local files, shell history, or retained logs.

Mitigation: Prefer a short-lived or revocable token, avoid pasting secrets into logged contexts, restrict local token file permissions, and rotate the token if exposure is suspected.

Risk: Input-escaping weaknesses may affect generated API payloads or shell commands.

Mitigation: Use the bundled JSON-building scripts or structured JSON payloads, inspect generated commands before running them, and avoid substituting untrusted text directly into shell syntax.

## Reference(s):

- [API command reference](artifact/references/api-commands.md)
- [Yinxiang authorization page](https://app.yinxiang.com/third/skills-oauth/)
- [ClawHub skill page](https://clawhub.ai/yinxiang-team/skills/yinxiang-skill)
- [Publisher profile](https://clawhub.ai/user/yinxiang-team)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown and natural-language responses with platform-specific bash or PowerShell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a user-provided Yinxiang token from YX_AUTH_TOKEN or a local token file; API responses are summarized for the user rather than shown as raw JSON.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
