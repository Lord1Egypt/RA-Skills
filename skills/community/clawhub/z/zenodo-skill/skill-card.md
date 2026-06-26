## Description: <br>
Helps agents deposit, publish, version, and search research artifacts on Zenodo through the Zenodo REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agents365-ai](https://clawhub.ai/user/agents365-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, researchers, and developers use this skill to create Zenodo deposits, upload files, set required metadata, publish citable DOI records, create new versions, and search published records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A production Zenodo publish or new-version publish is irreversible for files and records. <br>
Mitigation: Use the Zenodo sandbox for testing and require a final human review of files and metadata before any production publish action. <br>
Risk: The skill requires a Zenodo token with deposit permissions, which can create or modify records. <br>
Mitigation: Use the minimum required token scopes, prefer sandbox tokens during setup, pass tokens through environment variables, and keep tokens out of chat transcripts and files. <br>
Risk: Incorrect files or metadata could be attached to a citable DOI. <br>
Mitigation: Retrieve and review the draft deposition contents before publishing, especially title, creators, upload type, license, related identifiers, and uploaded filenames. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agents365-ai/zenodo-skill) <br>
- [Zenodo REST API Documentation](https://developers.zenodo.org) <br>
- [Zenodo Deposition Metadata Reference](references/metadata.md) <br>
- [Zenodo Search Reference](references/search.md) <br>
- [End-to-End Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include curl commands for Zenodo API calls, metadata JSON examples, search queries, DOI values, and record URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
