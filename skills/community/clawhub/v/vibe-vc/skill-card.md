## Description: <br>
Submit a vibe-coded startup to The Vibe VC, register project details, connect diligence integrations, relay human verification instructions, and use public newsletter or contact endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oliversum-ch](https://clawhub.ai/user/oliversum-ch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Founders, operators, and their agents use this skill to prepare a startup submission for The Vibe VC, send the registration payload with explicit human consent, and keep diligence evidence current through integrations. It also helps relay the required human verification post instructions after registration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can disclose startup, contact, repository, analytics, billing, or investor information to The Vibe VC endpoints. <br>
Mitigation: Run only with explicit human approval, review the dry-run payload first, and omit secrets or personal data that is not intended for disclosure. <br>
Risk: Integration connections may expose operational evidence surfaces such as repositories, workspaces, analytics, or billing systems. <br>
Mitigation: Use least-privilege access, prefer read-only or guest access where possible, and confirm the base URL before making API calls. <br>


## Reference(s): <br>
- [Vibe VC API + workflow reference](references/vibevc-api.md) <br>
- [Canonical Vibe VC skill reference](https://vibevc.md/skill.md) <br>
- [The Vibe VC](https://vibevc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper supports a dry-run mode to review the outbound payload before sending startup, contact, or integration details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
