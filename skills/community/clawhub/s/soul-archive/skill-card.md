## Description:

Soul Archive is a local-first digital personality and agent memory skill that extracts conversation-derived persona data, generates context prompts and reports, and helps agents recall patterns and warnings across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dqsjqian](https://clawhub.ai/user/dqsjqian)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use Soul Archive to maintain a local personal memory archive, inject concise persona context at session start, generate reports, and recall prior corrections or patterns before tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can build a long-lived plaintext personal profile and reuse it in future agent prompts.

Mitigation: Install only for intentional personal-memory use, review config.json before first use, and disable auto_extract, auto_reflect, or auto_context_inject when per-session control is required.

Risk: Sensitive personal details may later be included in prompts or exposed through local files.

Mitigation: Avoid storing health, financial, intimate, or other sensitive details unless acceptable, and keep the data directory out of public repositories and cloud sync services.

Risk: Any local agent with filesystem access may read or reuse the archive.

Mitigation: Limit use to trusted local agents and workspaces, and periodically inspect or delete plaintext JSON records that should no longer be retained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dqsjqian/skills/soul-archive)
- [Privacy documentation](PRIVACY.md)
- [Multi-device sync and backup](docs/multi-device-sync.md)
- [Extraction prompts](references/extraction_prompts.md)
- [Agent Guild](https://github.com/dqsjqian/agent-guild)
- [Claude Skills documentation](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/getting-started)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, HTML reports, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local plaintext JSON archive updates, persona prompts, memory recall summaries, warnings, and generated reports.]

## Skill Version(s):

3.2.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
