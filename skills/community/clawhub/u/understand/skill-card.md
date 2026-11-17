## Description:

Analyze a codebase to produce an interactive knowledge graph for understanding architecture, components, and relationships.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lum1104](https://clawhub.ai/user/lum1104)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze a repository and generate an interactive knowledge graph that explains source files, architecture layers, relationships, and a guided code tour.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads repository files, manifests, README content, directory listings, and git metadata to build its analysis.

Mitigation: Run it only on repositories whose contents are appropriate for local analysis, and review the generated knowledge graph before sharing it.

Risk: The skill runs generated local scripts during scanning, file extraction, architecture analysis, tour generation, and graph review.

Mitigation: Use a trusted or disposable workspace, inspect generated scripts when needed, and avoid running the skill on untrusted repositories.

Risk: The skill writes and removes files under .understand-anything/, including intermediate JSON and the final knowledge graph.

Mitigation: Back up or inspect any existing .understand-anything/ data before running the skill in an important workspace.

Risk: Repository text may influence the analysis prompts, and the security guidance notes weak prompt-injection handling.

Mitigation: Treat results from untrusted codebases as advisory, verify important conclusions manually, and do not follow unexpected commands surfaced through generated output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lum1104/skills/understand)
- [Skill definition](artifact/SKILL.md)
- [Project scanner prompt](artifact/project-scanner-prompt.md)
- [File analyzer prompt](artifact/file-analyzer-prompt.md)
- [Architecture analyzer prompt](artifact/architecture-analyzer-prompt.md)
- [Tour builder prompt](artifact/tour-builder-prompt.md)
- [Graph reviewer prompt](artifact/graph-reviewer-prompt.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown progress summary with JSON files written under .understand-anything/.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces .understand-anything/knowledge-graph.json and .understand-anything/meta.json; uses temporary intermediate JSON and local analysis scripts during execution.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
