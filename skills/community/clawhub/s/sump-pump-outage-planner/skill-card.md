## Description:

Use when a sump pump fails or the power goes out in a wet-basement house — estimates hours-to-critical water level from pit geometry and inflow rate, ranks response options by cost per hour of protection (battery backup vs generator vs water-powered), sizes a backup pump to actual inflow, and gives the failure-mode diagnostic tree (float stuck vs check valve vs impeller) with an emergency bailing plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT-0

## Use Case:

External homeowners with a sump pit can use the skill to estimate how long remains before water reaches a critical level during a pump failure or outage, compare backup options, and follow a basic failure triage plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Electrical troubleshooting around a suspected ground fault could expose people to electric shock.

Mitigation: Do not use an alternate-circuit workaround for a suspected ground fault. Have the electrical issue assessed by a qualified professional, preserve GFCI protection, follow manufacturer-approved float-testing instructions, and avoid electrical work while standing in water.

Risk: Runtime estimates and backup rankings may not match actual site conditions or equipment performance.

Mitigation: Treat backup rankings as rough runtime estimates, not cost comparisons; check actual equipment ratings and site conditions before relying on a plan.

## Reference(s):

- [Sump Pit Physics, Inflow Measurement, and Backup Engineering](references/pit-physics-and-backups.md)
- [ClawHub skill release](https://clawhub.ai/voronindenis5/skills/sump-pump-outage-planner)
- [Publisher profile](https://clawhub.ai/user/voronindenis5)
- [CDC flood electrical safety](https://www.cdc.gov/floods/safety/reentering-your-flooded-home-safety.html)

## Skill Output:

**Output Type(s):** [Analysis, Text, Guidance, Shell commands, JSON]

**Output Format:** [Triage and planning guidance, shell command examples, and optional JSON estimates from the included script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Estimates depend on user-supplied pit measurements, inflow assumptions, and backup equipment inputs.]

## Skill Version(s):

1.0.0 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
