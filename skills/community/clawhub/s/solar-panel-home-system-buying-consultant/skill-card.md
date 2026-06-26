## Description: <br>
Help users buying a home solar panel system calculate panel wattage, battery Ah, inverter VA, and charge controller type from their load, location, and grid situation - region-aware, brand-neutral. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arbazex](https://clawhub.ai/user/arbazex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External homeowners and residential buyers use this skill to size a home solar system before purchase. It gathers energy usage, location, roof, grid, and backup details, then returns component specifications and buying guidance that can be checked against installer quotes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The consultation asks for home, location, roof, energy-use, and backup details that could become sensitive if over-specific. <br>
Mitigation: Use approximate city or region and broad home details; avoid exact addresses, account numbers, personal identifiers, and unnecessary household information. <br>
Risk: Solar equipment specifications, certifications, incentives, permits, and grid-connection rules vary by region and change over time. <br>
Mitigation: Verify current component datasheets, local standards, utility rules, permits, incentives, and installer quotes with a qualified local solar professional before purchasing. <br>
Risk: Sizing output depends on user-provided consumption, roof, shade, and backup assumptions, so incomplete or inaccurate inputs can lead to over- or undersized recommendations. <br>
Mitigation: Collect recent bills or appliance load estimates, ask follow-up questions when inputs are vague, show calculations, and treat final specifications as estimates for professional review. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/arbazex/solar-panel-home-system-buying-consultant) <br>
- [Publisher profile](https://clawhub.ai/user/arbazex) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>
- [Declared project homepage](https://github.com/arbazex/power-energy-buying-consultants/tree/master/solar-panel-home-system-buying-consultant) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown consultation with formulas, tables, prioritized specifications, warnings, and matched system or product suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable output; recommendations depend on user-supplied home, location, load, and backup details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
