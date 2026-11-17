## Description:

Navigate Texas for living, moving, working, and road trips with region fit, state rules, weather risk, and daily logistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users use this skill for Texas-specific resident, relocation, travel, and business guidance, including regional tradeoffs, official workflow checks, weather readiness, local logistics, and practical checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional local memory under ~/texas/ can save sensitive personal context in plaintext.

Mitigation: Enable continuity only when needed, ask before creating files, and avoid saving credentials, SSNs, payment details, account numbers, immigration-status details, full addresses, or other sensitive identifiers.

Risk: Precise Texas rules and local workflows can change or depend on city, county, district, utility territory, or flood zone.

Mitigation: Use official state, local, district, and utility sources for current compliance steps; when verification is unavailable, avoid false precision.

Risk: Location-specific lookups may disclose ZIP, city, county, district, or school references to public services.

Mitigation: Use coarse location context when possible and send location details only when the user asks for location-specific guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/texas)
- [Texas.gov resident services](https://www.texas.gov/)
- [Texas DPS driver license services](https://www.dps.texas.gov/section/driver-license)
- [TxDMV new-to-Texas vehicle guidance](https://www.txdmv.gov/motorists/new-to-texas)
- [Texas Comptroller taxes portal](https://comptroller.texas.gov/)
- [Texas Education Agency](https://tea.texas.gov/)
- [Texas Ready preparedness guidance](https://www.texasready.gov/)
- [Power to Choose](https://www.powertochoose.org/)
- [FEMA flood maps](https://msc.fema.gov/)
- [ERCOT public grid conditions](https://www.ercot.com/)
- [Official Texas travel portal](https://www.traveltexas.com/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with checklists, links, and occasional shell commands for optional local memory setup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use optional local memory under ~/texas/ only after user confirmation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
