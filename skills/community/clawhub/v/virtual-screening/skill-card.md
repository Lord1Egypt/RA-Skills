## Description:

Virtual screening workflows for open and proprietary chemical libraries, including transformer-based screening and docking-based screening through SciMiner.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sciminer](https://clawhub.ai/user/sciminer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to choose and run SciMiner virtual-screening workflows for protein targets, using transformer-based screening from protein sequences or docking-based screening from receptor structures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent reads a SciMiner API key and uploads screening inputs to SciMiner.

Mitigation: Use a scoped SciMiner API key, keep it outside the repository, never print or persist it, and review which input files will be uploaded before invocation.

Risk: The skill relies on SciMiner-hosted Markdown that can change after review.

Mitigation: Review the selected remote API documentation before each run, or prefer a release that pins and validates the request-building documentation locally.

## Reference(s):

- [SciMiner tool API files](https://sciminer.tech/tool_api_files/)
- [SciMiner API key utility](https://sciminer.tech/utility)
- [Virtual Screening on ClawHub](https://clawhub.ai/sciminer/skills/virtual-screening)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, markdown]

**Output Format:** [Markdown with JSON snippets and runnable invocation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns SciMiner task status, task_id, result data, and share_url when a screening task succeeds.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
