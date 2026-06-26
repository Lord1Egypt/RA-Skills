## Description: <br>
Security scanner for ClawHub skills from Gen Digital. Looks up skill safety via the scan API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rexshang](https://clawhub.ai/user/rexshang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use Skillscanner to check ClawHub skill URLs against Gen Digital's scan API and decide whether to proceed, wait for review, or avoid a skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Skill URLs submitted for scanning are sent to an external scanner service. <br>
Mitigation: Submit only public ClawHub skill URLs unless the service is approved to receive private or access-controlled artifact URLs. <br>
Risk: A scanner verdict can miss obfuscated or novel threats, and pending analysis is not a clearance. <br>
Mitigation: Treat analysis_pending and non-SAFE severities as not cleared, and combine scan results with sandboxing, least privilege, and manual review. <br>


## Reference(s): <br>
- [Skillscanner on ClawHub](https://clawhub.ai/rexshang/skillscanner) <br>
- [Agent Trust Hub](https://ai.gendigital.com) <br>
- [Gen Digital scan lookup API](https://ai.gendigital.com/api/scan/lookup) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with bash curl commands and response interpretation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a ClawHub skill URL; treats analysis_pending and non-SAFE severities as not cleared.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
