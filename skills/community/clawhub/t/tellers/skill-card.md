## Description:

Create, edit, and share AI-generated videos using tellers.ai, including uploading media, generating videos, adding overlays, subtitles, music, and effects, exporting projects, and sharing previews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yxdunc](https://clawhub.ai/user/yxdunc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video creators use this skill to operate the Tellers CLI from an agent workflow for uploading footage, generating AI-assisted videos, exporting rendered projects, and sharing preview links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload private media through the Tellers CLI.

Mitigation: Confirm the files and paths selected for upload before running upload commands.

Risk: Upload, generation, and export operations may spend Tellers credits.

Mitigation: Confirm the intended operation and available credits before running long-running or paid CLI workflows.

Risk: Public preview commands can make an asset or project accessible to anyone with the link.

Mitigation: Only run anonymous-read or public-preview commands after confirming that public sharing is intended.

Risk: The skill requires a TELLERS_API_KEY credential.

Mitigation: Set the API key in the environment and avoid exposing it in prompts, logs, or generated output.

## Reference(s):

- [ClawHub Tellers Skill Page](https://clawhub.ai/yxdunc/skills/tellers)
- [Tellers API Documentation](https://www.tellers.ai/docs/dev/api)
- [Tellers Application](https://app.tellers.ai)
- [Tellers CLI Source](https://github.com/tellers-ai/tellers-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return asset IDs, project IDs, chat IDs, app URLs, export instructions, and public preview URLs from Tellers CLI workflows.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
