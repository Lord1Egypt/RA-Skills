## Description:

Zopia helps agents manage AI video and image creation projects on the Zopia platform, including scripts, character design, storyboards, multi-episode production, media generation, progress tracking, and result downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lambdua](https://clawhub.ai/user/lambdua)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and creative teams use this skill to create and manage Zopia projects for AI-assisted scripts, characters, storyboards, generated media, and rendered videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts, project metadata, generated assets, and the account token to Zopia.

Mitigation: Install and run it only for Zopia workflows you trust, and avoid submitting confidential or regulated content.

Risk: The skill can direct requests to a custom ZOPIA_BASE_URL.

Mitigation: Keep ZOPIA_BASE_URL at https://zopia.ai unless intentionally testing against a known local or controlled endpoint.

Risk: The skill downloads generated media files to the local filesystem.

Mitigation: Review downloaded images and videos before opening, sharing, or importing them into other tools.

Risk: The episode deletion script does not require an additional confirmation step.

Mitigation: Verify the episode ID and project context before running deletion commands.

## Reference(s):

- [Zopia skill page](https://clawhub.ai/lambdua/skills/zopia)
- [Zopia platform](https://zopia.ai)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, JSON, files]

**Output Format:** [Markdown guidance with shell commands, JSON command output, project URLs, and downloaded image or video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and ZOPIA_ACCESS_KEY; ZOPIA_BASE_URL defaults to the official HTTPS endpoint.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
