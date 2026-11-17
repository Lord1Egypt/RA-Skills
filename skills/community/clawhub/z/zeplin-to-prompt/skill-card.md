## Description:

Export one or more Zeplin screen URLs into a structured layer tree with local assets and package the result as a zip file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sullivangu](https://clawhub.ai/user/sullivangu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to export Zeplin screen links into local prompt-ready design packages with layer JSON, an HTML preview, and assets for AI-assisted UI implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Zeplin personal access tokens for project exports.

Mitigation: Prefer ZEPLIN_TOKEN through an environment variable or another local secret mechanism, avoid pasting tokens into chat, and delete ~/.zeplin-skill-config.json when finished.

Risk: Local command-launching paths and custom work directories require care.

Mitigation: Use --no-open when running scripts directly and avoid attacker-controlled --workdir paths until shell-based open calls are reviewed.

Risk: Exports can contain private Zeplin design data and downloaded assets.

Mitigation: Use tokens scoped to the relevant project and share generated ZIP files only with intended recipients.

## Reference(s):

- [Zeplin to Prompt ClawHub Skill](https://clawhub.ai/sullivangu/skills/zeplin-to-prompt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline shell commands plus generated JSON, HTML, local assets, and ZIP files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exports may include raw Zeplin response data, minified layer-tree JSON, preview HTML, downloaded assets, and a ZIP package.]

## Skill Version(s):

1.0.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
