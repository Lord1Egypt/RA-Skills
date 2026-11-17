## Description:

Helps an agent deposit, publish, version, and search research artifacts on Zenodo through the REST API, including DOI-minting workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agents365-ai](https://clawhub.ai/user/agents365-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and research operations teams use this skill to create Zenodo depositions, upload files, set metadata, publish records, mint DOIs, create new versions, discard drafts, and search public Zenodo records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a Zenodo personal access token to create deposits, upload files, publish records, create versions, or discard drafts.

Mitigation: Install it only when Zenodo account automation is intended, keep production tokens limited to required scopes, and avoid exposing tokens in commands or files.

Risk: Publishing to production Zenodo is irreversible for uploaded files and records.

Mitigation: Use sandbox tokens for first-time workflows and require explicit user confirmation before production publish actions.

Risk: Incorrect files or metadata could be published with a DOI.

Mitigation: Review deposition files and metadata with the user before publish, and correct Zenodo validation errors before continuing.

Risk: Draft file deletion during versioning can remove intended inherited files from the new draft.

Mitigation: Require explicit confirmation before draft file deletion and inspect the draft state after changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agents365-ai/skills/zenodo-skill)
- [Zenodo REST API Documentation](https://developers.zenodo.org)
- [Zenodo Deposition Metadata Reference](references/metadata.md)
- [Zenodo Search Reference](references/search.md)
- [End-to-end examples](references/examples.md)
- [GitHub archiving and citation documentation](https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, JSON request bodies, and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Zenodo REST API endpoints, curl commands, metadata JSON, confirmation prompts, DOI values, and record URLs.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
