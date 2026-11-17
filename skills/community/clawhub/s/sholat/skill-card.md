## Description:

Mengambil jadwal sholat untuk kota atau kabupaten di Indonesia dari api.myquran.com, termasuk imsak, subuh, dzuhur, ashar, maghrib, isya, dan pencarian ID lokasi.

This skill is ready for commercial/non-commercial use.

## Publisher:

[banghasan](https://clawhub.ai/user/banghasan)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to retrieve Indonesian prayer times for today, a specific date, or a monthly period by city/regency keyword or location ID.

### Deployment Geography for Use:

Global; functional coverage is limited to Indonesian cities and regencies supported by api.myquran.com.

## Known Risks and Mitigations:

Risk: Location keywords, location IDs, requested dates/months, and timezone values are sent to api.myquran.com.

Mitigation: Use the skill only when sharing those request details with api.myquran.com is acceptable.

Risk: Monthly requests in the helper script currently show a 7-day preview rather than a full month.

Mitigation: Treat monthly helper output as a preview and use the underlying API response or additional calls when a complete month is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/banghasan/skills/sholat)
- [api.myquran.com v3 API](https://api.myquran.com/v3)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown-style text with optional shell commands and concise prayer-time lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Indonesian location and prayer-time output; the helper script prints only the first 7 days for monthly requests.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
