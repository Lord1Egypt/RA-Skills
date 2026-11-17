## Description:

TrailSnap CLI helps agents query and manage TrailSnap photos, albums, tags, locations, people, storage folders, and media through the bundled Python CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lc044](https://clawhub.ai/user/lc044)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users working with a TrailSnap deployment use this skill to configure API access, search photo collections, inspect albums, tags, locations, people, and folders, and retrieve media when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delete photos through the TrailSnap API.

Mitigation: Require explicit human approval before running `photos delete`, and use a least-privilege TrailSnap token where possible.

Risk: The skill stores the TrailSnap API URL and token in a plaintext `.env` file inside the artifact directory.

Mitigation: Protect the workspace, avoid sharing the artifact directory, and rotate the token if the file may have been exposed.

Risk: `medias get --format file` can write downloaded media to a local path.

Mitigation: Use an explicit safe output path and require human approval before allowing an agent to write media files.

Risk: Non-local HTTP endpoints can expose tokens or photo metadata to unintended services.

Mitigation: Prefer local or trusted HTTPS TrailSnap endpoints and verify the configured API URL before use.

## Reference(s):

- [Command reference](artifact/reference.md)
- [Usage examples](artifact/examples/simple.md)
- [ClawHub skill page](https://clawhub.ai/lc044/skills/trailsnap-cli)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Text, Files]

**Output Format:** [CLI stdout as JSON or text, with optional base64 or file media output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured TrailSnap API URL and bearer token before API-backed commands can run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
