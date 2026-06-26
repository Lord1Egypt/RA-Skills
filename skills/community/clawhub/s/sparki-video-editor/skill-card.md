## Description: <br>
AI video editor for creators that helps transform raw footage into polished vlogs, talking-head videos, short-form social clips, captions, translations, and style-cloned edits through the Sparki CLI and hosted editing workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sparki-io](https://clawhub.ai/user/sparki-io) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agent users use this skill to configure Sparki, upload or select video assets, choose editing preferences, run hosted video edits, monitor project status, download results, and manage uploaded assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow uploads selected videos or reference URLs to Sparki-hosted editing services, so it is not appropriate for footage that must remain fully local or private. <br>
Mitigation: Use only with videos the user is comfortable sending to Sparki, and confirm the upload source before running upload or edit commands. <br>
Risk: The skill requires a Sparki API key and installs the Sparki CLI from PyPI. <br>
Mitigation: Install only when the publisher is trusted, store the API key through the documented setup flow, and run `sparki doctor` before editing. <br>
Risk: The workflow can involve credit top-ups or asset deletion steps. <br>
Mitigation: Ask for explicit user confirmation before purchase-related or destructive asset deletion commands. <br>


## Reference(s): <br>
- [Sparki homepage](https://sparki.io) <br>
- [Sparki Telegram bot](https://t.me/Sparki_AI_bot) <br>
- [ClawHub skill page](https://clawhub.ai/sparki-io/sparki-video-editor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides the agent through Sparki CLI setup, uploads, editing modes, polling, downloads, and asset cleanup.] <br>

## Skill Version(s): <br>
1.1.0 (source: server evidence, SKILL.md frontmatter, pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
