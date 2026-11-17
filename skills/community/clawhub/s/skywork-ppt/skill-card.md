## Description:

Skywork PPT helps agents generate new PowerPoint presentations, imitate an existing presentation style, edit decks through natural-language requests, convert NotebookLM exports to editable PPTX files, and run local PPTX operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gxcun17](https://clawhub.ai/user/gxcun17)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to create, transform, and inspect PowerPoint presentations from topics, templates, existing decks, NotebookLM exports, and local PPTX files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Skywork-backed workflows may send selected prompts and files to Skywork or cloud storage.

Mitigation: Use only with content approved for that service, and avoid confidential decks unless organizational policy permits it.

Risk: The skill requires a Skywork API key for remote workflows.

Mitigation: Store the key in a protected secret store, use a revocable key, and avoid printing it in logs.

Risk: Local slide-editing operations can modify presentation files.

Mitigation: Use explicit output paths or keep backups before running operations that may overwrite local decks.

Risk: The security verdict is suspicious because the skill uploads local documents and can modify files without strong safeguards.

Mitigation: Review the skill before deployment and run dependencies in a virtual environment.

## Reference(s):

- [Skywork API key setup](references/apikey-fetch.md)
- [Skywork AI](https://skywork.ai)
- [ClawHub skill page](https://clawhub.ai/gxcun17/skills/skywork-ppt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands and generated or modified PPTX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and SKYWORK_API_KEY for Skywork-backed workflows; local PPTX operations use python-pptx.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
