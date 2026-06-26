## Description: <br>
Raindrop.io bookmark and collection manager for a local OpenClaw workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stanestane](https://clawhub.ai/user/stanestane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to manage Raindrop.io bookmarks and collections from a local workspace, including authentication checks, collection organization, bookmark search, and import or export workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Raindrop.io credentials and can save OAuth tokens in a local plaintext env file. <br>
Mitigation: Prefer user environment variables or a protected local env file, use --no-save when tokens should not be written to disk, and restrict access to any file containing tokens. <br>
Risk: The CLI can modify or delete live collections and bookmarks. <br>
Mitigation: Verify collection and bookmark IDs before update, delete, or bulk import commands, and test bulk changes on a small set before applying them broadly. <br>


## Reference(s): <br>
- [API notes](references/api-notes.md) <br>
- [Optional local env file example](references/env-example.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; CLI commands may return text, JSON, CSV, or local files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide local API-backed bookmark operations and import/export files when the user runs the provided CLI commands.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
