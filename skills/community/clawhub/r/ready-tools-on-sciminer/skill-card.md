## Description:

Discover a user-specified SciMiner tool from the published API-doc index, read its Markdown description, and invoke it through the SciMiner internal API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sciminer](https://clawhub.ai/user/sciminer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to discover SciMiner tool API documentation, collect exact invocation parameters, submit authenticated SciMiner jobs, handle documented file uploads, and return shareable result links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live remote tool documentation controls authenticated SciMiner requests.

Mitigation: Review the resolved tool documentation before invocation and verify requests stay on the intended SciMiner API host.

Risk: Authenticated uploads could expose user files if the selected tool documentation changes or is compromised.

Mitigation: Avoid uploading sensitive files and confirm required upload fields before submitting jobs.

Risk: A stored SciMiner API key could be misused if overprivileged or exposed.

Mitigation: Use a revocable, least-privilege SciMiner API key and do not print, persist, or store the key in prompts, logs, or repository files.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/sciminer/skills/ready-tools-on-sciminer)
- [SciMiner tool API documentation index](https://sciminer.tech/tool_api_files/)
- [SciMiner API key utility](https://sciminer.tech/utility)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with JSON result summaries and optional code or shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include SciMiner task IDs and share_url values; must not expose API keys.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
