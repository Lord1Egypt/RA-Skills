## Description:

Scenario-driven skill recommendation engine for ClawHub. Detects failed or stuck workflows, builds targeted search queries, and returns ranked skill recommendations with immediate recovery steps and fallback paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackleeio](https://clawhub.ai/user/jackleeio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Skill Feed when a workflow is blocked by an error, timeout, retry loop, missing output, or unclear implementation path. It turns the failure context into sanitized ClawHub search queries, ranked skill recommendations, immediate recovery steps, and a fallback path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Troubleshooting context may contain secrets, credentials, PII, or internal details before it is converted into search queries.

Mitigation: Strip sensitive values and keep only generic error codes, error types, platform names, and action verbs before searching or sharing output.

Risk: Recommended skills may have their own permissions, setup costs, or security posture.

Mitigation: Review and scan each recommended skill before installing it or granting runtime permissions.

Risk: Offline fallback recommendations can become stale.

Mitigation: Use the bundled top-skills snapshot only as a fallback and re-check ClawHub live search before final recommendations when available.

## Reference(s):

- [Skill Feed on ClawHub](https://clawhub.ai/jackleeio/skills/skill-feed)
- [ClawHub skill search](https://clawhub.ai/skills?focus=search)
- [ClawHub skills by stars](https://clawhub.ai/skills?sort=stars&dir=desc)
- [ClawHub skills by recent updates](https://clawhub.ai/skills?sort=updatedAt&dir=desc)
- [Discovery Workflow](references/discovery-workflow.md)
- [Query Templates](references/query-templates.md)
- [Provider Adaptation Guide](references/provider-adaptation.md)
- [Top Skills Snapshot](references/top-skills-2026-03-09.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown recovery plan with ranked recommendations, immediate actions, success checks, fallback path, and provider-adapted execution notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search queries and troubleshooting context should be sanitized before external use.]

## Skill Version(s):

0.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
