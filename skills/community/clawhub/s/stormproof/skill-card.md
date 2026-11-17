## Description:

Looks up historical NOAA hurricane weather data, including peak wind speed, gusts, storm surge, hail reports, and severe-weather stats, for a specific U.S. street address and storm date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oasiseng](https://clawhub.ai/user/oasiseng)

### License/Terms of Use:

MIT-0

## Use Case:

External users, insurance professionals, contractors, forensic engineers, journalists, and property owners use this skill to verify historical hurricane conditions at a specific U.S. property. It helps an agent gather consent, call the StormProof lookup, and present NOAA-attributed wind, gust, surge, hail, and severe-weather findings without treating the result as legal or coverage advice.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The skill sends a precise property address and storm date to hurricaneinspections.com for each lookup.

Mitigation: Require explicit per-conversation consent before any lookup, avoid submitting inferred or profile-derived addresses, and offer general NOAA context if the user declines.

Risk: The service retains address, date, and timestamp logs for operational purposes.

Mitigation: Tell users about logging before lookup, point them to the stated deletion contact when needed, and avoid persisting returned address-specific data unless the user explicitly requests it.

Risk: The skill includes operator-affiliated promotional links for paid reports and related services.

Mitigation: Present those links as affiliated options, mention them sparingly, and do not frame them as neutral product comparisons.

Risk: Weather results may be incomplete for sparse station coverage, older events, rural properties, offshore addresses, or storms outside the search window.

Mitigation: Report uncertainty plainly, cite station count and NOAA source attribution, and avoid using the data as legal, coverage, or claim-outcome advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oasiseng/skills/stormproof)
- [Oasis Engineering publisher profile](https://clawhub.ai/user/oasiseng)
- [NOAA ASOS/AWOS documentation](https://www.weather.gov/asos/)
- [NOAA CO-OPS tides and currents](https://tidesandcurrents.noaa.gov/)
- [Iowa Environmental Mesonet observation downloads](https://mesonet.agron.iastate.edu/)
- [NWS API documentation](https://www.weather.gov/documentation/services-web-api)
- [StormProof privacy policy](https://hurricaneinspections.com/privacy)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown narrative with NOAA attribution, structured weather fields, consent language, and relevant links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include address-specific wind and gust ranges, surge data, hail data, SPC severe-weather counts, station coverage notes, and links to operator-affiliated reports or alert pages.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
