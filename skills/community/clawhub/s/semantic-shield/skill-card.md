## Description:

Semantic Shield lets agents and developers query an API for safety scores, risk levels, threat details, and install recommendations before using AI skills, plugins, or MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simplysemantics](https://clawhub.ai/user/simplysemantics)

### License/Terms of Use:

MIT

## Use Case:

Developers, agent builders, and security teams use this skill to check the trust profile of AI skills, plugins, and MCP tools before installation or autonomous use. They can also submit unvetted public skills for expert evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an external SaaS service and requires a vendor API key.

Mitigation: Use a scoped, revocable Semantic Shield API key and review vendor availability and privacy requirements before relying on the service in production workflows.

Risk: Validation requests send skill identifiers, provider names, and optional public skill URLs to the service.

Mitigation: Submit only public skill metadata and do not include private repositories, internal URLs, secrets, source code, or user personal data.

## Reference(s):

- [Semantic Shield product page](https://www.simplysemantics.com/semantic-shield.html)
- [Semantic Shield ClawHub listing](https://clawhub.ai/simplysemantics/skills/semantic-shield)
- [Simply Semantics publisher profile](https://clawhub.ai/user/simplysemantics)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown trust reports with API request guidance and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SEMANTIC_SHIELD_API_KEY and uses skill_id, provider, and optional public skill_url inputs.]

## Skill Version(s):

1.0.1 (source: server release and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
