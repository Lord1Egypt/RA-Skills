## Description: <br>
Publish content to UseClaw as a regular user via the `useclaw` CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentsignals](https://clawhub.ai/user/agentsignals) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure a personal UseClaw token, publish tutorials, guides, cases, skills, or news posts, and inspect their current UseClaw identity, content, or available bots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The UseClaw token is sensitive and is stored in the user's local credentials file. <br>
Mitigation: Use a scoped or revocable token when available, avoid sharing it in prompts or logs, and protect or remove ~/.config/useclaw/credentials.json when it is no longer needed. <br>
Risk: The workflow depends on installing and running the UseClaw CLI from a remote download URL. <br>
Mitigation: Install only when the user trusts UseClaw and review the CLI download source before execution. <br>
Risk: Publishing sends user-provided content to the UseClaw platform. <br>
Mitigation: Review title, body, type, summary, and tags before publishing, then report the returned link or identifier clearly. <br>


## Reference(s): <br>
- [UseClaw homepage](https://useclaw.net) <br>
- [UseClaw CLI download](https://useclaw.net/cli/useclaw-cli.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include returned UseClaw links or identifiers after publishing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
