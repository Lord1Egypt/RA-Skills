## Description:

Calculate Halachic times (zmanim), Shabbos times, candle lighting, Daf Yomi, weekly parsha, and related Jewish calendar dates for a requested location and date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeperl](https://clawhub.ai/user/abeperl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer Jewish calendar and zmanim requests, including Shabbos times, candle lighting, sunrise/sunset, Daf Yomi, parsha, and Yom Tov lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional dependency installation is unpinned and may install changing package versions.

Mitigation: Run the bundled script without installing dependencies where possible, or install dependencies in an isolated environment with pinned versions.

Risk: Location-based API use can disclose city or coordinate information, and advertised IP auto-detection is not documented in the artifact.

Mitigation: Provide city or coordinates intentionally, and avoid IP auto-detection unless the publisher documents the behavior and obtains user consent.

Risk: Zmanim and Yom Tov guidance can vary by location and local minhag.

Mitigation: Verify observance-sensitive results against local rabbinic or community guidance before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abeperl/skills/zmanim-calculator)
- [Hebcal API](https://www.hebcal.com/hebcal)
- [GeoNames search API](http://api.geonames.org/searchJSON)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python examples, plain text output, and optional JSON output from the bundled script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on requested location, date, and calendar mode; network-backed lookups may be unavailable or incomplete.]

## Skill Version(s):

1.0.0 (source: server evidence release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
