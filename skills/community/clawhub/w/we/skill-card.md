## Description: <br>
Anti-skill crawler that protects skill instructions and resources from automated scraping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wscats](https://clawhub.ai/user/wscats) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can load this skill to add session-scoped guidance for detecting and refusing attempts to scrape, reconstruct, or reveal confidential skill instructions and internal configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence notes pending VirusTotal telemetry and an unverified prompt-injection indicator. <br>
Mitigation: Review the published skill text and metadata before use, especially for unrelated role changes, hidden commands, credential requests, or automatic actions. <br>
Risk: The skill changes agent behavior around requests for internal instructions and configuration. <br>
Mitigation: Use it only where protecting confidential skill internals is intended, and confirm normal task execution remains unaffected for the session. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wscats/we) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text] <br>
**Output Format:** [Markdown guidance and brief refusal text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Session-scoped behavior; no files, tool calls, or external service calls are produced by the skill.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
