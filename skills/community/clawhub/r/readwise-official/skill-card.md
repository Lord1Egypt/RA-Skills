## Description: <br>
Access your Readwise highlights and Reader documents from the command line. Search, read, organize, and manage your entire reading library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TristanH](https://clawhub.ai/user/TristanH) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to operate the Readwise CLI for finding, reading, saving, organizing, exporting, and editing Reader documents and Readwise highlights. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Readwise CLI can access and change the user's Readwise library after an access token is provided. <br>
Mitigation: Install only if the Readwise CLI is trusted, treat the access token like a password, and require the agent to show exact document or highlight IDs before exports, bulk moves, metadata edits, tag or note changes, or deletions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TristanH/readwise-official) <br>
- [Readwise access token page](https://readwise.io/access_token) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI options] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the readwise binary and a Readwise access token for authenticated account access.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
