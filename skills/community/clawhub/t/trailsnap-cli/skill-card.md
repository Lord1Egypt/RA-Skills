## Description: <br>
TrailSnap CLI lets an agent query TrailSnap photos, albums, tags, locations, people, storage folders, and media through the bundled Python CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lc044](https://clawhub.ai/user/lc044) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to inspect and manage a TrailSnap photo library from an agent workflow, including photo search, metadata lookup, album, tag, location, people, folder, and media retrieval tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes a photo deletion command without built-in confirmation. <br>
Mitigation: Require explicit human confirmation before running any photo deletion command. <br>
Risk: The skill stores a TrailSnap API token in a local .env file. <br>
Mitigation: Use a least-privileged API token and protect the local .env file from disclosure. <br>
Risk: The skill can access private photo-library metadata and media through the configured TrailSnap account. <br>
Mitigation: Install and run it only where the agent is trusted with the associated TrailSnap account and photo library. <br>


## Reference(s): <br>
- [TrailSnap CLI command reference](reference.md) <br>
- [TrailSnap CLI examples](examples/simple.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON, files] <br>
**Output Format:** [CLI output as JSON or text, with optional media URLs, base64 data, or saved files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured TrailSnap API URL and bearer token before API-backed commands can run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
