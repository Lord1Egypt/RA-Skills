## Description: <br>
Execute AI workflow orchestration flows using the AetherLang Omega DSL for multi-step AI pipelines across recipes, business strategy, market analysis, molecular gastronomy, and related analysis tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[contrario](https://clawhub.ai/user/contrario) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to build and submit AetherLang workflow DSL flows that call an external orchestration API and return structured AI-generated results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided flow code and query text are sent to api.neurodoc.app for processing. <br>
Mitigation: Inform users before the first API call and send only the minimum flow code and explicit query text needed for the task. <br>
Risk: Sensitive personal data, credentials, private files, or confidential business information could be exposed if included in the request text. <br>
Mitigation: Review and strip sensitive content before sending requests to the external service. <br>
Risk: External API availability, rate limits, or server errors can prevent workflow execution. <br>
Mitigation: Handle 400, 413, 429, and 500 responses clearly and avoid retrying requests that include sensitive or unnecessary data. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/contrario/skills-2) <br>
- [Publisher homepage](https://masterswarm.net) <br>
- [AetherLang API endpoint](https://api.neurodoc.app/aetherlang/execute) <br>
- [Aether Nexus Omega DSL page](https://neurodoc.app/aether-nexus-omega-dsl) <br>
- [Artifact-declared security middleware source](https://github.com/contrario/aetherlang/blob/main/aetherlang/middleware/security.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown and structured text from external API responses, with AetherLang DSL code examples where needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-provided flow code and query text; no credentials are required by the packaged skill.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
