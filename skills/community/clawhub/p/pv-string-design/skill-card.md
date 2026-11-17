## Description:

Calculates photovoltaic module string counts, checks inverter voltage, current, and DC/AC sizing, and recommends PV string configurations using conservative and irradiance-temperature coupled methods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuepeng1985-web](https://clawhub.ai/user/yuepeng1985-web)

### License/Terms of Use:

MIT-0

## Use Case:

Solar engineers, developers, and external users can use this skill to prepare photovoltaic string design reports from module, inverter, and project-location inputs. It helps compare configurations, recommend string counts, and document voltage, current, temperature, and DC/AC ratio checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect photovoltaic string calculations could produce unsafe design recommendations.

Mitigation: Require independent engineering verification before using the reported configuration for procurement, installation, or operation.

Risk: Temperature coefficient units may be misunderstood or inconsistently normalized.

Mitigation: Confirm whether coefficients are provided as percent per degree Celsius or decimal values before applying voltage corrections.

Risk: Per-MPPT current limits may be exceeded when multiple strings are connected to the same tracker.

Mitigation: Check aggregate current for each MPPT input and compare it against inverter limits before accepting a configuration.

Risk: Automatic weather or location lookup can disclose project-location data or use unreliable local temperature data.

Mitigation: Ask for confirmation before external lookup and cite authoritative weather sources for extreme-temperature assumptions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuepeng1985-web/skills/pv-string-design)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown report with tables and calculation summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes configuration comparisons, recommended string counts, and voltage/current validation tables.]

## Skill Version(s):

1.0.1 (source: server release metadata, created 2026-04-28T09:31:52Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
