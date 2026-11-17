## Description:

Sparki is an AI video editor for creators that turns raw footage into polished vlogs, talking-head videos, captions, translations, social clips, and style-cloned edits through chat or automated ClawBot workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sparki-io](https://clawhub.ai/user/sparki-io)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, social media teams, and agents use this skill to turn raw local or uploaded video into edited vlogs, clips, captions, translations, and style-cloned social content through Sparki CLI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs mutable external CLI code from PyPI.

Mitigation: Use a pinned and reviewed Sparki CLI release for production workflows, and run `sparki doctor` to verify the installed skill version before commands are executed.

Risk: Video files, reference files, prompts, and task metadata may be sent through Sparki cloud and Telegram workflows.

Mitigation: Use the skill only when external processing is acceptable, verify returned upload links, and avoid sensitive or regulated videos unless the data handling path has been approved.

Risk: The skill requests access to local working-directory reads, local configuration and video output writes, and network access to Sparki services.

Mitigation: Run it from the intended working directory, review the configured filesystem paths, and limit use to trusted Sparki API endpoints.

## Reference(s):

- [Sparki homepage](https://sparki.io)
- [Sparki Telegram bot](https://t.me/Sparki_AI_bot)
- [ClawHub skill page](https://clawhub.ai/sparki-io/skills/sparki-video-editor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides Sparki CLI setup, upload, edit, status, download, and storage-management flows; completed video files are downloaded by the CLI.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter, pyproject.toml, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
