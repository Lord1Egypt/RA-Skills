## Description:

Chat-driven SaaS idea discovery and validation pipeline that generates idea seeds, runs discovery, critique, and evaluation agents, and produces scored, ranked PRDs with founder-aware ranking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itthomas](https://clawhub.ai/user/itthomas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, founders, and product teams use this skill to explore a SaaS domain, generate eight candidate ideas, and stress-test them through discovery, adversarial critique, scoring, and contextual ranking before deeper validation work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided text may be used in file paths that are later placed into shell commands without clear sanitization.

Mitigation: Use simple alphanumeric domain names, avoid shell metacharacters in prompts, generate safe slugs for run directories, and verify paths stay under saas-scout-runs.

Risk: The cron watchdog may continue running if a skill run is stopped early.

Mitigation: Confirm the watchdog is removed when a run is stopped or after evaluation completes.

Risk: Shell string assembly around generated paths can increase command execution risk.

Mitigation: Replace shell string assembly with safer file operations where possible and review before installing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/itthomas/skills/saas-idea-scout)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with PRDs, critiques, evaluations, dossiers, ranked summaries, inline shell commands, and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates run artifacts under saas-scout-runs, including context, pool files, dossiers, and model preference configuration.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
