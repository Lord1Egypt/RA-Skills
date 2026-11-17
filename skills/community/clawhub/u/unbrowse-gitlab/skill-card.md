## Description:

Connects agents to Unbrowse tools for GitLab pricing, project discovery, and documentation lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unbrowse](https://clawhub.ai/user/unbrowse)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other GitLab users can retrieve pricing information, find projects by name, and read GitLab documentation through an agent. The integration also offers broader browser-assisted tasks when a listed tool does not fit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The remote service may receive OAuth or API-key access and run authenticated GitLab browser sessions.

Mitigation: Connect only when comfortable granting that access, and keep API keys in a secret manager rather than committed configuration.

Risk: Browser-assisted fallback can extend beyond the listed read-only lookups and potentially change account or project state.

Mitigation: Require explicit user confirmation before login, tool-compilation fallback, or any state-changing action.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/unbrowse/skills/unbrowse-gitlab)
- [Unbrowse GitLab integration](https://unbrowse.ai/sites/gitlab.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Text or Markdown with retrieved page content and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include pricing data, project search results, and documentation page titles and links.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
