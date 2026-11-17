## Description:

Reddit Skills helps an agent operate Reddit through a local CLI and browser extension for authentication checks, publishing, search and discovery, social interactions, and compound content workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1146345502](https://clawhub.ai/user/1146345502)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to search Reddit, inspect posts and profiles, publish posts, comment, vote, save content, and run multi-step Reddit content operations from an agent interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local browser bridge can control a logged-in Reddit session.

Mitigation: Use a dedicated Reddit account or Chrome profile, keep the bridge stopped and the extension disabled when not in use, and review actions before running them.

Risk: Automated posting, commenting, voting, or saving can affect a real Reddit account and may trigger platform limits or restrictions.

Mitigation: Manually confirm every post, comment, vote, and save action, and keep operation frequency low.

Risk: Image posting can process user-specified URLs or local file paths.

Mitigation: Avoid arbitrary image URLs and sensitive local paths until stricter URL, file, and bridge authentication controls are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1146345502/skills/reddit-skills)
- [Project homepage](https://github.com/1146345502/reddit-skills)
- [README](README.md)
- [Skill definition](SKILL.md)
- [Chrome extension manifest](extension/manifest.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and structured summaries of JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent responses may include proposed Reddit actions that should be reviewed before execution.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
