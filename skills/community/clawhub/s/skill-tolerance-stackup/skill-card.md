## Description:

Tolerance Stackup helps dimensional, process, and design engineers calculate one-dimensional tolerance stack-ups using Worst Case and RSS methods, verify assembly gaps or interference, and identify major contributors to tolerance overruns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Dimensional, process, and design engineers use this skill to evaluate one-dimensional assembly tolerance chains, compare Worst Case and RSS results against gap or interference requirements, and decide where tolerance contribution is highest. It is a calculation aid for engineering review, not a substitute for final design approval or 3D tolerance analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect or unverified dimensions, tolerance directions, distribution assumptions, or assembly requirements could produce misleading engineering recommendations.

Mitigation: Treat outputs as a calculation aid; confirm all inputs, assumptions, WC/RSS applicability, and final decisions through qualified engineering review.

Risk: The artifact references scripts/build_report.py, but no executable helper is bundled in the release evidence.

Mitigation: Avoid executing any local scripts/build_report.py unless it is intentionally provided by a trusted source and reviewed before use.

## Reference(s):

- [Source repository](https://github.com/duding-engicool/skill-tolerance-stackup)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-tolerance-stackup)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown and plain text calculation reports with formulas, tables, assumptions, WC/RSS results, requirement checks, and tolerance contribution notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided component dimensions, tolerances, chain directions, and assembly gap or interference requirements; missing requirements are flagged for follow-up.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
