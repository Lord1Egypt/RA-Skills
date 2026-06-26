## Description: <br>
Store and recall persistent memories via FlightBox on the Quack Network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JPaulGrayson](https://clawhub.ai/user/JPaulGrayson) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to store, search, list, and delete persistent memory entries through FlightBox when they need context to carry across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and retrieves memory through a cloud-backed FlightBox service using a local Quack credential. <br>
Mitigation: Install only if the publisher and FlightBox service are trusted, and avoid storing secrets, regulated data, private personal information, or sensitive business context unless remote persistence is intentional. <br>
Risk: Stored memories can become stale or no longer appropriate for future sessions. <br>
Mitigation: Review recalled memories before relying on them and delete memories that are no longer needed. <br>


## Reference(s): <br>
- [Quack Memory on ClawHub](https://clawhub.ai/JPaulGrayson/quack-memory) <br>
- [FlightBox API](https://flightbox.replit.app/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Terminal text and JSON responses from memory commands, with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local Quack credential and network access to the FlightBox API.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
