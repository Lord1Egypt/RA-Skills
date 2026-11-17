## Description:

Gets daily Islamic prayer times for UK locations using location lookup and the Aladhan prayer-times API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clinicode](https://clawhub.ai/user/clinicode)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to look up Fajr, Sunrise, Dhuhr, Asr, Maghrib, and Isha times for UK cities, towns, boroughs, and neighborhoods. It supports auto-detected location or a manually supplied UK location.

### Deployment Geography for Use:

United Kingdom

## Known Risks and Mitigations:

Risk: Auto-detecting location contacts an IP geolocation service and may reveal IP-derived location information.

Mitigation: Use a manually supplied broad UK city or area when avoiding IP-derived location sharing is preferred.

Risk: Manual location lookup contacts an external geocoder before prayer times are fetched.

Mitigation: Avoid entering precise addresses; use city, town, borough, or neighborhood names.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/clinicode/skills/uk-prayer-times)
- [Aladhan Timings API](https://api.aladhan.com/v1/timings)
- [ipapi IP Geolocation API](https://ipapi.co/json/)
- [OpenStreetMap Nominatim Search](https://nominatim.openstreetmap.org/search)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text prayer-time table with optional command-line examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shows six daily prayer-related times in 12-hour AM/PM format and includes the resolved location and date.]

## Skill Version(s):

1.4.4 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
