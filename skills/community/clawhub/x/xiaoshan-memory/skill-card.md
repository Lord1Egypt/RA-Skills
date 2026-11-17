## Description:

XiaoShan Memory Engine provides persistent AI memory with semantic search, knowledge graph features, and analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waychan8](https://clawhub.ai/user/waychan8)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to give an agent persistent local memory by saving, semantically searching, asking over, and deleting memory records through a local XiaoShan Memory Engine service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install and update path references @latest installation and an external HTTP engine/update source, while the engine is not bundled in the artifact.

Mitigation: Review and verify the external engine/update source before installation, and prefer a pinned, integrity-checked installer or package version.

Risk: Saved memories and search or question prompts may contain sensitive user data, and provider data flow is not fully disclosed.

Mitigation: Treat memory content and queries as sensitive, configure provider credentials deliberately, and prefer local processing where appropriate.

Risk: The /forget endpoint behavior is not fully described, so deletion may not remove every related record or derived representation.

Mitigation: Confirm exactly what /forget deletes before relying on it for privacy, retention, or compliance workflows.

Risk: License activation stores the provided key under the local .xiaoshan directory, and the security evidence flags secret-handling concerns.

Mitigation: Avoid using valuable license keys until storage permissions and secret handling are reviewed and improved.

## Reference(s):

- [XiaoShan Memory Engine HTTP API Reference](references/api.md)
- [ClawHub skill page](https://clawhub.ai/waychan8/skills/xiaoshan-memory)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration guidance, API usage guidance]

**Output Format:** [Markdown with HTTP endpoint guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may direct agents to call a local HTTP service at 127.0.0.1:18790 and to use local provider configuration.]

## Skill Version(s):

3.3.0 (source: evidence release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
