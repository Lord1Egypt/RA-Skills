## Description: <br>
Helps agents use tella-cli to manage Tella videos, clips, playlists, exports, transcripts, collaborators, and webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[melvynx](https://clawhub.ai/user/melvynx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content teams, and workspace operators use this skill to automate Tella workspace tasks such as listing videos, editing clips, exporting recordings, retrieving transcripts, managing playlists, and configuring webhooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Tella API key and can access workspace videos, transcripts, playlists, sharing settings, webhook secrets, and collaborator controls. <br>
Mitigation: Use a least-privileged Tella API key where possible and avoid exposing API keys or webhook secrets in chat or logs. <br>
Risk: The skill supports destructive or sensitive operations such as deletes, collaborator changes, sharing changes, exports, and webhook secret retrieval. <br>
Mitigation: Require explicit confirmation before performing destructive actions or changing access, sharing, export, or webhook-secret settings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/melvynx/tella-cli) <br>
- [Tella API key settings](https://www.tella.tv/settings/api-keys) <br>
- [Bun installer](https://bun.sh/install) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent workflows should use --json for parseable command output.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
