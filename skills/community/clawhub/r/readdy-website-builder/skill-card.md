## Description:

Provides CLI-based website creation and management through the Readdy.ai platform, including project creation, modification, preview, publishing, listing, and deletion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frankready2025](https://clawhub.ai/user/frankready2025)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate Readdy.ai website projects from an agent, including generating new sites, modifying existing projects, previewing builds, publishing selected versions, and deleting projects when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a Readdy account API key, and setup can expose the key through shell history or process logs.

Mitigation: Configure the key only in a trusted shell, clear sensitive command history when appropriate, and rotate the API key if exposure is suspected.

Risk: Publish and delete operations can materially affect remote Readdy projects.

Mitigation: Confirm the exact project ID and selected version before publishing, and require explicit user confirmation before deleting a project.

Risk: Website prompts and project history may store or reuse prior prompt content and generated event data.

Mitigation: Do not include passwords, tokens, private customer data, or other secrets in website generation or modification prompts.

## Reference(s):

- [Readdy.ai](https://readdy.ai)
- [Readdy API Reference](references/API.md)
- [Readdy API Key](https://readdy.ai/user/api-key)
- [ClawHub Skill Page](https://clawhub.ai/frankready2025/skills/readdy-website-builder)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and Readdy project status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include project IDs, version IDs, preview URLs, publish status, and error guidance from the Readdy CLI.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
