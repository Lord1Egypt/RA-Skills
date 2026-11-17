## Description:

Helps agents search, compare, recommend, and install ClawHub skills for think-tank research workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sapereaude2014](https://clawhub.ai/user/sapereaude2014)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, analysts, and developers use this skill to find suitable ClawHub skills for industry research, academic research, news monitoring, report writing, visualization, PDF, spreadsheet, and presentation workflows. It can also install curated research skill bundles in restricted or standard mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can add multiple unverified remote skills into the active agent skills folder without per-package confirmation.

Mitigation: Install only trusted skill sources, review the bundle list before execution, and prefer the default restricted mode.

Risk: Custom registry, workdir, or dir values can change where skills are installed or which registry supplies them.

Mitigation: Avoid custom registry and directory values unless required, and inspect installed skills before using them.

Risk: A mirror miss can trigger fallback to another registry.

Mitigation: Review installer output and verify each installed skill with ClawHub before enabling it in normal workflows.

## Reference(s):

- [ThinkTank Skill Finder on ClawHub](https://clawhub.ai/sapereaude2014/skills/thinktank-skill-finder)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with structured recommendations and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce ClawHub search, install, and verification commands; executing installer commands can add skills to the active agent skills directory.]

## Skill Version(s):

1.0.9 (source: server release metadata and SKILL.md heading)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
