## Description:

Connects Gmail, Calendar, Drive, Atlassian, Notion, GitHub, Salesforce, and other enterprise tools through a single Venn MCP endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ninonano64](https://clawhub.ai/user/ninonano64)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and teams use this skill to authenticate with Venn, discover connected enterprise SaaS services, and coordinate work across tools such as Gmail, Jira, Notion, GitHub, and Salesforce from an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer runs unverified code from a mutable third-party GitHub branch before handling OAuth-backed enterprise service access.

Mitigation: Review the installer and dependency source before use; prefer a release that pins a reviewed commit or signed release.

Risk: The skill can participate in authenticated access to connected enterprise SaaS services.

Mitigation: Use it only with trusted Venn URLs, keep activation tied to explicit @venn requests, and require user confirmation for operations marked as audited writes.

Risk: Local setup creates persistent vennporter files and configuration used for future authenticated sessions.

Mitigation: Disclose and review the files created under the user's local home directory and remove them when access is no longer needed.

## Reference(s):

- [Venn](https://venn.ai)
- [Venn OpenClaw Assistant Settings](https://app.venn.ai/assistants/openclaw)
- [Venn MCP Endpoint](https://app.venn.ai/mcp)
- [mcporter Installer Dependency](https://github.com/mansilladev/mcporter.git)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VENN_UNIVERSAL_URL and the vennporter command-line tool before Venn-backed actions can run.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 1.0.4 and _meta.json lists 1.0.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
