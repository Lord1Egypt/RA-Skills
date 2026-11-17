## Description:

Create AI-First Website with GEO (Generative Engine Optimization) and marketing rules to convert visitors into leads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galizki](https://clawhub.ai/user/galizki)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to generate AI-optimized EvoWeb sites from business descriptions, then receive hosted site and editor URLs after polling the EvoWeb API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Business descriptions may be sent to EvoWeb as a third-party hosted service.

Mitigation: Confirm the user is authorized to share the business information before invoking the API, and exclude secrets, regulated information, private customer data, or confidential plans unless explicitly approved.

Risk: Website generation may consume EvoWeb account credits.

Mitigation: Confirm credit use is acceptable before starting generation or retrying a failed site.

Risk: Generated websites may become hosted on EvoWeb infrastructure.

Mitigation: Tell the user where the generated site will be hosted and provide the editor URL so they can review or modify the result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/galizki/skills/sell-evoweb-ai)
- [EvoWeb website and API key registration](https://evoweb.ai/?utm_source=claw&utm_medium=skill&utm_campaign=selfselling&utm_content=v1.0)
- [EvoWeb API base URL](https://api.evoweb.ai/openapi/api/v1)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, Guidance]

**Output Format:** [Markdown with hosted website and editor URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EVOWEB_API_KEY and may consume EvoWeb account credits.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
