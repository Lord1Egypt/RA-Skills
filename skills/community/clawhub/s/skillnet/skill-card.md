## Description:

Search, download, create, evaluate, and analyze reusable agent skills via SkillNet, an open skill supply chain for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[icarus-chen](https://clawhub.ai/user/icarus-chen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to find existing reusable skills, download and review relevant third-party skill content, create new skills from repositories, documents, prompts, or logs, and evaluate or organize a local skill library.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send repository metadata, document text, trajectory logs, and skill snippets to the configured LLM endpoint during create, evaluate, and analyze workflows.

Mitigation: Confirm the exact BASE_URL and data volume before use; redact sensitive content or use a local LLM endpoint for confidential material.

Risk: Installation instructions use an unpinned skillnet-ai package, which may change behavior across releases.

Mitigation: Install with pipx in an isolated environment and pin a trusted skillnet-ai version where reproducibility matters.

Risk: Downloaded skills and scripts are third-party content that may contain unsafe operational instructions.

Mitigation: Review file listings, SKILL.md previews, and full scripts before loading or running anything; treat downloaded scripts as reference material unless explicitly approved.

Risk: Credential misuse could expose LLM API keys or GitHub tokens if environment routing is misconfigured.

Mitigation: Use short-lived, least-privilege credentials and verify API_KEY, BASE_URL, and GITHUB_TOKEN scope before sensitive commands.

## Reference(s):

- [SkillNet API and CLI Reference](references/api-reference.md)
- [SkillNet Security and Privacy Reference](references/security-privacy.md)
- [SkillNet Workflow Patterns](references/workflow-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/icarus-chen/skills/skillnet)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, code snippets, and generated local skill files or JSON reports when helper commands are used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search returns matching skill metadata; create writes skill directories; evaluate returns quality ratings; analyze can write relationships.json.]

## Skill Version(s):

2.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
