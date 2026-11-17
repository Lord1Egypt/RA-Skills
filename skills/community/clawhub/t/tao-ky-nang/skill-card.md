## Description:

Huong dan tao ky nang Claude. Su dung khi muon xay dung skill, tao ky nang, viet YAML, hoac kiểm thu ky nang.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nguyenhoang11032002-ai](https://clawhub.ai/user/nguyenhoang11032002-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this Vietnamese guide to plan, write, validate, test, and publish Claude skills with clear frontmatter, folder structure, examples, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Skill templates copied from the guide may trigger too broadly or activate on unrelated requests.

Mitigation: Use narrow trigger phrases, include negative triggers where useful, and test activation against both obvious and unrelated prompts before publishing.

Risk: Examples involving MCP or external service workflows may lead an agent to propose changes outside the user's intended scope.

Mitigation: Require explicit user confirmation before creating or modifying external resources, and verify the connected MCP server, credentials, and tool names first.

Risk: The bundled validator inspects a local folder and reads SKILL.md content from that path.

Mitigation: Run the validator only on skill folders the user intends to inspect and review reported frontmatter issues before upload.

## Reference(s):

- [Template Examples](references/template-examples.md)
- [YAML Frontmatter](references/yaml-frontmatter.md)
- [ClawHub Skill Page](https://clawhub.ai/nguyenhoang11032002-ai/skills/tao-ky-nang)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with YAML, Markdown, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Vietnamese-language instructional output for creating and validating skills.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
