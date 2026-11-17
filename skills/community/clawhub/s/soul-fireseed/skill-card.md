## Description:

Soul Fireseed helps an agent extract personality signals from conversations or memory records, build structured persona profiles, and generate evolution reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sanzhishuyuan](https://clawhub.ai/user/sanzhishuyuan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent analyze conversations or selected memory records, extract six-dimensional personality features, and produce persona snapshots, stored fossils, and evolution reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill intentionally analyzes conversations into persistent personality profiles.

Mitigation: Install only when that profiling behavior is desired, store generated outputs in protected locations, and review extracted records before relying on them.

Risk: Background and historical memory analysis may process more user context than expected.

Mitigation: Prefer manual mode and run historical scans only on explicitly selected data.

Risk: The authoritative security summary flags unsafe helper scripts and a suspicious overall verdict.

Mitigation: Do not run the shell scripts with untrusted filenames or arguments until they are reviewed and fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sanzhishuyuan/skills/soul-fireseed)
- [FireSeed homepage](https://fireseed.online)
- [Skill guide](artifact/SKILL.md)
- [Usage guide](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, structured JSON fossils and persona profiles, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist personality fossils, persona profiles, backups, and generated reports under user-data paths when used with the bundled code.]

## Skill Version(s):

2.1.0 (source: evidence release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
