## Description:

Image recognition using Ollama + qwen3.5:4b with think=False for reliable content extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huruilizhen](https://clawhub.ai/user/huruilizhen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Vision Tool to analyze selected image files through a configured Ollama qwen3.5:4b service and return visual descriptions or structured JSON results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images and prompts are sent to the configured Ollama service.

Mitigation: Keep Ollama local for sensitive images and analyze only images the user intends to share with that service.

Risk: Development cleanup commands can remove local build and cache files when run in a modified workspace.

Mitigation: Review cleanup commands before running them and keep unrelated work outside the skill workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huruilizhen/skills/vision-tool)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [Plain text image analysis or JSON result object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [JSON output includes success or error status, source, elapsed time, token statistics, image name, prompt, and analysis text when available.]

## Skill Version(s):

1.1.3 (source: server release metadata, SKILL.md frontmatter, CHANGELOG; pyproject.toml reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
