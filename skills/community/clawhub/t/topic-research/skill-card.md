## Description:

Run a second-hop deep research pass through the Tavily CLI after an initial scan, then normalize the result into a local `research.md` contract.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abigale-cyber](https://clawhub.ai/user/abigale-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to deepen a chosen topic after an initial news scan, produce a cited research report, and generate writing-decision guidance for follow-up content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release guidance asks users to install Tavily CLI through a remote shell installer.

Mitigation: Review the installer before use or choose a safer Tavily CLI installation method when available.

Risk: `source_file` can point to local content whose excerpt may be sent to Tavily and retained in raw JSON output.

Mitigation: Use only intended inbox files as sources and avoid secrets, private notes, internal documents, environment files, or paths outside the expected workspace.

Risk: Untrusted request files can control research fields such as topic, question, seed URLs, and source file path.

Mitigation: Review request files before execution and reject unexpected source paths or seed URLs.

## Reference(s):

- [ClawHub Topic Research release](https://clawhub.ai/abigale-cyber/skills/topic-research)
- [Tavily CLI installer](https://cli.tavily.com/install.sh)

## Skill Output:

**Output Type(s):** [markdown, json, guidance]

**Output Format:** [Markdown research report plus raw JSON trace file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a normalized research report and raw Tavily JSON under content-production/inbox/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
