## Description:

Search and read Twitter/X profiles, tweets, trends, and Spaces through the AISA relay, then publish OAuth-approved posts with selected media files using AISA_API_KEY.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill for Twitter/X research, monitoring, and user-approved posting without handling Twitter passwords. It is intended for workflows that can send search terms, OAuth state, post content, and selected media files through the AISA relay.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Twitter/X content, search terms, OAuth state, post content, and selected media files may be sent through the AISA relay.

Mitigation: Install and use this skill only when the user trusts the AISA relay and accepts that data flow.

Risk: AISA_API_KEY can appear in command output.

Mitigation: Avoid running the skill in logged environments and rotate the key if it has already been exposed.

Risk: Media upload commands can read and upload local files when paths are provided.

Mitigation: Pass only explicit user-selected workspace files with media upload options.

## Reference(s):

- [OpenClaw Twitter OAuth](references/post_twitter.md)
- [OpenClaw](https://openclaw.ai)
- [ClawHub Skill Page](https://clawhub.ai/bibaofeng/skills/twitter-aisa-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and network access to the AISA relay.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
