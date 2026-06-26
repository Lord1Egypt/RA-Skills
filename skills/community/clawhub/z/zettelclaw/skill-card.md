## Description: <br>
Work inside a Zettelclaw vault using the current typed frontmatter schema, inbox + Base workflows, and human-write/agent-read guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxpetretta](https://clawhub.ai/user/maxpetretta) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent search, organize, and update a Zettelclaw note vault while preserving typed frontmatter, inbox triage, journal scaffolding, and human-write boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent actions could move, delete, or change note status in a user's vault. <br>
Mitigation: Review and explicitly approve proposed moves, deletes, and status changes before applying them. <br>
Risk: Vault search or organization may expose local notes and memory paths to the active agent session. <br>
Mitigation: Install only for vaults the user is comfortable letting an agent search and help organize. <br>
Risk: Incorrect OpenClaw memory-path configuration could broaden what the agent can search. <br>
Mitigation: Review OpenClaw memory-path changes and use only the documented agents.defaults.memorySearch.extraPaths setting when configuration is requested. <br>


## Reference(s): <br>
- [Zettelclaw on ClawHub](https://clawhub.ai/maxpetretta/zettelclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with YAML frontmatter, wikilinks, search command snippets, and optional configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; does not install software or require credentials.] <br>

## Skill Version(s): <br>
2026.3.11 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
