## Description:

Soil science, composting, and water management for food production. Use when someone wants to improve their garden soil, start composting, set up irrigation, harvest rainwater, or scale up food growing beyond containers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to guide garden soil testing, composting, fertility building, irrigation setup, rainwater harvesting, and drainage decisions for food-growing areas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release declares filesystem access without a clear need for ordinary gardening guidance.

Mitigation: Install in an environment where filesystem permissions can be reviewed or scoped before use.

Risk: The install path uses an unpinned npx command.

Mitigation: Review the package source and run installation from a non-privileged shell with sensitive environment variables minimized.

Risk: Rainwater harvesting rules and composting programs vary by jurisdiction.

Mitigation: Check local regulations and extension or municipal programs before recommending collection systems or location-specific practices.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/howtousehumans/skills/soil-water-management)
- [USDA Cooperative Extension System](https://www.nifa.usda.gov/about-nifa/how-we-work/extension/cooperative-extension-system)
- [Irrigation Association](https://www.irrigation.org/)
- [American Rainwater Catchment Systems Association](https://www.arcsa.org/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown guidance with structured checklists, code-fenced state snippets, and action triggers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May tailor advice by jurisdiction, measurement system, climate zone, soil test result, garden scale, and budget.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
