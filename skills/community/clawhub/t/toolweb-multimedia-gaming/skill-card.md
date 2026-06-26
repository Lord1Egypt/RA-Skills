## Description: <br>
AI-powered platform that generates personalized career roadmaps for multimedia and gaming professionals based on skills assessment and learning goals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, career counselors, training providers, educational institutions, and talent-development teams use this skill to generate multimedia and gaming career roadmaps, specialization recommendations, learning paths, milestones, and next steps from assessment data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends career assessment details, session IDs, optional user IDs, skills, goals, and experience information to an external third-party API. <br>
Mitigation: Use pseudonymous session and user identifiers where possible, and avoid sending confidential employer, client, or personally sensitive information. <br>
Risk: The release carries crypto and purchase capability tags, but the security evidence does not document a clear need for wallet, crypto, purchase, or payment authority. <br>
Mitigation: Do not grant wallet, crypto, purchase, or payment authority unless the publisher separately documents a specific operational need. <br>


## Reference(s): <br>
- [OpenAPI specification](artifact/openapi.json) <br>
- [API Docs](https://api.mkkpro.com:8184/docs) <br>
- [Kong Route](https://api.mkkpro.com/career/multimedia-gaming) <br>
- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-multimedia-gaming) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, JSON] <br>
**Output Format:** [JSON API responses with career roadmap guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include profile summaries, skill gaps, specialization recommendations, phased learning paths, milestones, estimated timelines, and next steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and OpenAPI info.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
