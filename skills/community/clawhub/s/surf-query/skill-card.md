## Description: <br>
Surf Query helps agents answer Taiwan surf spot queries with spot details, nearby spot lookup, tide, wind, typhoon, sunrise and sunset information, map links, and optional parking lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Harperbot](https://clawhub.ai/user/Harperbot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and OpenClaw operators use this skill to find Taiwan surf spots by name, region, or GPS coordinates and receive practical surf conditions, map links, and optional nearby parking results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes an unverified self-updater. <br>
Mitigation: Audit or disable update.sh before installation, avoid cron-based updater execution, and prefer platform-reviewed or pinned updates. <br>
Risk: CWA requests use an API key while TLS verification is disabled. <br>
Mitigation: Use a low-privilege CWA API key and review network behavior before enabling live CWA data. <br>
Risk: Parking lookup executes a separately installed skill when parking mode is used. <br>
Mitigation: Install and review parking_query separately before enabling parking mode. <br>


## Reference(s): <br>
- [ClawHub Surf Query Listing](https://clawhub.ai/Harperbot/surf-query) <br>
- [CWA Open Data](https://opendata.cwa.gov.tw) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [parking_query Optional Integration](https://github.com/Harperbot/openclaw-parking-query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Plain text surf reports with map URLs and status lines suitable for chat channels] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May omit live tide, wind, and typhoon data when CWA_API_KEY is not configured.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and surf_query.py version comment) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
