## Description: <br>
Watchboard Intelligence queries watchboard.dev for structured tracker data, KPIs, contested claims, recent events, and daily digests across conflict, politics, culture, science, space, and historical topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[artemiopadilla](https://clawhub.ai/user/artemiopadilla) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve structured Watchboard intelligence for covered trackers, including briefings, casualty figures, KPIs, contested claims, breaking tracker summaries, recent events, search results, and RSS fallbacks. It is best suited to topics covered by Watchboard and should not be treated as authoritative for breaking news less than about 24 hours old. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Watchboard responses are external intelligence content and may include contested or outdated claims. <br>
Mitigation: Verify high-stakes claims with primary sources and review contested KPI notes before relying on the output. <br>
Risk: The skill contacts watchboard.dev and stores temporary public API or RSS responses in /tmp/watchboard-cache. <br>
Mitigation: Use only in environments where outbound access to watchboard.dev and temporary local caching of public responses are acceptable. <br>
Risk: The artifact notes that Watchboard is not intended for breaking news less than about 24 hours old. <br>
Mitigation: Use the skill for covered trackers with daily or periodic updates, and supplement very recent events with primary or time-sensitive sources. <br>


## Reference(s): <br>
- [Watchboard](https://watchboard.dev) <br>
- [Watchboard API v1](https://watchboard.dev/api/v1/) <br>
- [ClawHub release page](https://clawhub.ai/artemiopadilla/watchboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Terminal text summaries or raw JSON from a Python CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries public Watchboard API and RSS endpoints, supports optional JSON mode, and caches public responses locally in /tmp/watchboard-cache for one hour.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
