## Description: <br>
Finds and compares bookable hotels near a known landmark using POI anchoring, radius filters, and distance or rating sorting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel planners and end users use this skill to turn a city, landmark, dates, and optional budget or radius preferences into nearby hotel recommendations with comparison tables, images, and booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports authenticated local-bridge or browser-session control capabilities that may let the assistant operate active sessions. <br>
Mitigation: Install only if you trust the local bridge, protect ZCLAW_API_KEY and local configuration files, and limit use to accounts and pages you intend the assistant to operate. <br>
Risk: Hotel availability, prices, distances, and booking terms may change after search results are produced. <br>
Mitigation: Ask the user to verify dates, price, cancellation terms, and location details on the booking page before making a reservation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/travel-accommodation-advisor) <br>
- [FlyAI homepage](https://open.fly.ai/) <br>
- [Playbooks](references/playbooks.md) <br>
- [Templates](references/templates.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with hotel comparison tables, images, booking links, and optional execution logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses city, landmark, dates, radius, budget, hotel stars, and sorting preferences; booking links should use detailUrl when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
