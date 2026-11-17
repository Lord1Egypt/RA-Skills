## Description:

查詢台灣全島衝浪浪點資訊，含即時潮汐、風況、颱風動態、日出日落，可附帶查詢附近停車場。支援 Telegram、LINE、iMessage。

This skill is ready for commercial/non-commercial use.

## Publisher:

[harperbot](https://clawhub.ai/user/harperbot)

### License/Terms of Use:

MIT

## Use Case:

External OpenClaw users use this skill to look up Taiwan surf spots by name, region, or nearby GPS coordinates, including surf conditions, tide and wind context, sunrise and sunset times, map links, and optional nearby parking information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled updater retrieves replacement files without signed or pinned release verification.

Mitigation: Do not use the updater until it verifies signed or pinned releases; install updates through a reviewed release process.

Risk: Live CWA requests disable HTTPS certificate verification while sending an API key.

Mitigation: Avoid live CWA features on untrusted networks until TLS verification is restored; use offline lookup or a trusted network when possible.

Risk: Optional cron notifications and parking integration can send surf or location-adjacent information through external channels or local companion skills.

Mitigation: Enable those features only for known recipients and trusted local skills, and scope notification jobs narrowly.

## Reference(s):

- [CWA Open Data](https://opendata.cwa.gov.tw)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [parking_query optional integration](https://github.com/Harperbot/openclaw-parking-query)
- [ClawHub Surf Query page](https://clawhub.ai/harperbot/skills/surf-query)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain text surf reports with map URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live CWA tide, wind, weather, and typhoon data when CWA_API_KEY is configured; offline surf-spot lookup remains available without the key.]

## Skill Version(s):

1.2.0 (source: server release metadata and surf_query.py version comment)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
