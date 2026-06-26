## Description: <br>
NotebookLM CLI wrapper via `node {baseDir}/scripts/notebooklm.mjs`. Use for auth, notebooks, chat, sources, notes, sharing, research, and artifact generation/download. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Fadeloo](https://clawhub.ai/user/Fadeloo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to operate NotebookLM through an installed CLI for authentication, notebook management, chat, source handling, notes, sharing, research, and artifact generation or download. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a user's logged-in NotebookLM account through an external CLI. <br>
Mitigation: Install only when the external NotebookLM CLI is trusted and the intended account access is acceptable. <br>
Risk: Commands can delete content, export artifacts, change collaborators, enable public sharing, change language settings, or bypass prompts with `--yes`. <br>
Mitigation: Require explicit confirmation before destructive, sharing, export, collaborator, language-change, or `--yes` commands. <br>


## Reference(s): <br>
- [NotebookLM CLI command catalog](references/cli-commands.md) <br>
- [ClawHub skill page](https://clawhub.ai/Fadeloo/tiangong-notebooklm-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown, JSON, Files] <br>
**Output Format:** [Markdown guidance with shell commands; wrapped CLI commands may emit text, JSON, or downloaded files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, the notebooklm CLI on PATH, and an authenticated NotebookLM session.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
