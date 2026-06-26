## Description: <br>
Skill Feed is a scenario-driven ClawHub skill recommendation agent that detects failed or unclear workflows, builds sanitized search queries, and returns ranked skill recommendations with recovery steps and fallback paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackleeio](https://clawhub.ai/user/jackleeio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Skill Feed when a workflow fails, times out, lacks an expected output, or has no clear implementation path. The skill helps them search ClawHub, compare candidate skills, and choose a primary recommendation, alternatives, immediate actions, success checks, and a fallback path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive details from a failed workflow could be included in generated search terms. <br>
Mitigation: Review generated search terms when context is sensitive; the skill instructs agents to strip secrets, credentials, PII, internal URLs, private paths, request bodies, response bodies, and authorization headers before search. <br>
Risk: Recommended downstream skills may require separate trust, setup, or permission decisions. <br>
Mitigation: Evaluate each recommended skill separately before installing it or granting permissions. <br>


## Reference(s): <br>
- [Skill Feed ClawHub Page](https://clawhub.ai/jackleeio/skill-feed) <br>
- [Discovery Workflow](references/discovery-workflow.md) <br>
- [Query Templates](references/query-templates.md) <br>
- [Provider Adaptation](references/provider-adaptation.md) <br>
- [Top Skills Snapshot](references/top-skills-2026-03-09.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown recovery plan with ranked recommendations, immediate actions, success checks, fallback guidance, and provider-specific execution notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses sanitized failure context and avoids repeating the same recommendation for the same error within one conversation.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
