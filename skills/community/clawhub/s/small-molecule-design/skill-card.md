## Description:

Small-molecule generation workflows combining REINVENT4, PocketXMol, fpocket, and Gnina Score through SciMiner.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sciminer](https://clawhub.ai/user/sciminer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and computational chemistry researchers use this skill to generate, optimize, and validate small molecules through SciMiner-hosted REINVENT4, PocketXMol, fpocket, and Gnina Score workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable remote SciMiner documentation controls authenticated API calls and file uploads.

Mitigation: Review the selected SciMiner documentation before each run, restrict calls to the documented SciMiner endpoints, and prefer versions that vendor fixed schemas or validate remote docs against a strict allowlist.

Risk: SciMiner workflows require an API key and may upload molecular structures or receptor files.

Mitigation: Use a narrowly scoped, revocable SciMiner API key stored outside the repository, avoid exposing it in prompts or logs, and do not upload sensitive unpublished structures unless the SciMiner documentation source is trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sciminer/skills/small-molecule-design)
- [SciMiner tool API files](https://sciminer.tech/tool_api_files/)
- [REINVENT4 API documentation](https://sciminer.tech/tool_api_files/REINVENT4_api_doc.md)
- [PocketXMol API documentation](https://sciminer.tech/tool_api_files/PocketXMol_api_doc.md)
- [fpocket API documentation](https://sciminer.tech/tool_api_files/fpocket_api_doc.md)
- [Gnina Score API documentation](https://sciminer.tech/tool_api_files/Gnina%20Score_api_doc.md)
- [SciMiner API key utility](https://sciminer.tech/utility)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON examples and code or shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful SciMiner task summaries should include task identifiers and share_url links.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
