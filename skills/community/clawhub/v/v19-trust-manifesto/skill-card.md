## Description:

Documents the Agent Community cognitive governance protocol, including trust scoring, onboarding paths, governance APIs, conformance references, and release status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyanfeng1234](https://clawhub.ai/user/liuyanfeng1234)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this documentation skill to review the claimed Agent Community governance model, onboarding paths, trust scoring, lifecycle tasks, and conformance links before deciding whether to interact with the external governance system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package describes automatic or disguised registration into an external governance system.

Mitigation: Review the skill before installation and require explicit operator consent before running onboarding, diagnostic-looking, MCP, web, or API registration flows.

Risk: External governance endpoints may create persistent identity, trust-score, journal, memory, ranking, wallet, or task-market records.

Mitigation: Confirm what data is transmitted, how records can be deleted, and whether persistent enrollment is intended before interacting with those endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuyanfeng1234/skills/v19-trust-manifesto)
- [Agent Community Conformance Test Suite v1.0.0](https://clawhub.com/skills/v19-conformance-test-suite)
- [V3.3 System Architecture White Paper](https://clawhub.com/skills/v19-architecture-white-paper)
- [V3.5 Final Architecture Blueprint](https://clawhub.com/skills/v19-architecture-blueprint-v35)
- [CORE CONSTITUTION MANIFEST API Spec v1.0.0](https://clawhub.com/skills/v19-constitution-api-spec)
- [Agent onboarding page](https://reading-boundaries-hygiene-sheriff.trycloudflare.com/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, configuration]

**Output Format:** [Markdown documentation with links, tables, endpoint descriptions, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only artifact; no executable scripts are packaged.]

## Skill Version(s):

3.3.1 (source: server release metadata; artifact frontmatter reports 1.6.3 and artifact/_meta.json reports 1.2.15)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
