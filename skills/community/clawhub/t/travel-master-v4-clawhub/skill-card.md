## Description: <br>
TravelMaster V4 helps agents collect travel requirements, converge on a plan, and generate responsive HTML travel guides with merchant and navigation links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timo2026](https://clawhub.ai/user/timo2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to gather trip preferences, compare local plan options, and produce an HTML itinerary-style guide with travel, venue, and merchant links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated merchant or payment links could be incorrect or unsafe to use directly. <br>
Mitigation: Manually verify every merchant, booking, payment, and navigation link before booking, paying, or sharing the output. <br>
Risk: The release includes real API and travel-service claims that may require credentials and operational review. <br>
Mitigation: Use limited-scope API keys, avoid unnecessary sensitive travel details, and validate third-party API behavior in a controlled environment before deployment. <br>
Risk: Background-start or watchdog-style service instructions may create unmanaged long-running processes. <br>
Mitigation: Do not run watchdog commands unless the supplied script is present and reviewed; use an explicitly managed service such as systemd or supervisor when deployment is needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/timo2026/travel-master-v4-clawhub) <br>
- [Amap location services](https://lbs.amap.com) <br>
- [FlyAI](https://flyai.com) <br>
- [Tencent location services](https://lbs.qq.com) <br>
- [Meituan Open Platform](https://open.meituan.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and generated HTML travel-report content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include merchant, navigation, and API-backed travel links that should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
