## Description:

Allocates N objects across T rounds among K options by ratio, maximizing coverage diversity and supporting post-processing modes for repeat distribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ldxs001](https://clawhub.ai/user/ldxs001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to create balanced recurring allocations for projects, students, users, or other objects across rounds and options. It produces allocation reports and visualizations for review, adjustment, and export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports may expose users to script execution risks from unescaped custom labels and CDN-loaded JavaScript.

Mitigation: Avoid untrusted custom label text, inspect reports before opening, and use --no-html or --no-open for sensitive data until escaping, pinned local dependencies or SRI are added.

Risk: Persistently bypassing confirmation can allow incorrect allocation parameters to run without review.

Mitigation: Keep confirmation enabled for normal use and avoid --always unless the workflow and input source are trusted.

Risk: Very large allocation inputs can reduce performance because hard input limits are not enforced by the security evidence.

Mitigation: Stay within the documented operating range, such as N <= 1000 objects, T <= 52 rounds, and K <= 20 options, until hard limits are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ldxs001/skills/round-robin-allocator)
- [Usage guide](references/usage.md)
- [Algorithm notes](references/algorithm.md)
- [FAQ and troubleshooting](references/faq.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Markdown, HTML, CSV, Shell commands, Configuration]

**Output Format:** [Markdown allocation report, optional CSV export, and interactive HTML visualization; may include CLI commands and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python >= 3.8. HTML visualizations load Chart.js and Plotly.js from CDN unless HTML output is disabled.]

## Skill Version(s):

1.6.0 (source: release evidence, SKILL.md frontmatter, _meta.json, changelog released 2026-06-10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
