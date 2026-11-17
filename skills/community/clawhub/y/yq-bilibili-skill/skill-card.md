## Description:

Provides agent-facing Bilibili CLI workflows for retrieving video, subtitle, AI summary, comment, related-video, audio, user, search, ranking, feed, favorites, history, and account interaction data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianheihei002](https://clawhub.ai/user/tianheihei002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate the bilibili-cli tool for Bilibili content lookup, audio extraction, structured YAML or JSON output, authenticated library access, and explicit account interactions such as likes, coins, triples, and unfollows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can reuse saved Bilibili credentials or browser cookies.

Mitigation: Use QR login or a dedicated browser/profile where possible, and install only when the agent is allowed to access that Bilibili login state.

Risk: The skill includes account-changing actions such as likes, coins, triples, and unfollows.

Mitigation: Require explicit user confirmation before any authenticated or account-changing command is executed.

Risk: Ambiguous user requests could trigger unintended authenticated actions.

Mitigation: Clarify the intended operation and target video or user before running commands that modify account state.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tianheihei002/skills/yq-bilibili-skill)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Text]

**Output Format:** [Markdown with inline shell commands and YAML/JSON output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide commands that produce subtitles, SRT files, segmented WAV audio, full m4a audio, YAML, or JSON through bilibili-cli.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
