## Description:

Turn YouTube videos into structured, reusable skill files that make any AI agent smarter. Forge, compound, and recall creator-attributed knowledge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[koren-source](https://clawhub.ai/user/koren-source)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to convert YouTube transcripts into reusable skill files, maintain a local SkillForge library, and recall creator-attributed knowledge through CLI or MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation depends on an external npm package whose exact reviewed version is not pinned in the artifact evidence.

Mitigation: Prefer a pinned package version, verified provenance, or a sandboxed install before use in environments with strong supply-chain controls.

Risk: The skill creates local library, configuration, proposal, and search-index files under ~/.skillforge/.

Mitigation: Review the first-run consent prompt and confirm the target output path before allowing writes.

## Reference(s):

- [YouTube SkillForge ClawHub release](https://clawhub.ai/koren-source/skills/youtube-skillforge)
- [koren-source ClawHub publisher profile](https://clawhub.ai/user/koren-source)
- [youtube-skillforge npm package](https://www.npmjs.com/package/youtube-skillforge)
- [yt-dlp Homebrew formula](https://formulae.brew.sh/formula/yt-dlp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown skill files, CLI text output, and MCP JSON-RPC tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local SkillForge library files under ~/.skillforge/ after user consent; uses yt-dlp and the user's configured agent LLM provider.]

## Skill Version(s):

4.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
