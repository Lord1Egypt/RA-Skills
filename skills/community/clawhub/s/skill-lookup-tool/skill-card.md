## Description:

Search, retrieve, and install Agent Skills from the prompts.chat registry using MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhengxinjipai](https://clawhub.ai/user/zhengxinjipai)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI-agent users use this skill to search the prompts.chat registry, compare skill results, retrieve selected skills, and install them into Claude skill directories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing registry content can write untrusted files into an agent skill-loading directory.

Mitigation: Use only trusted registries and publishers; require a visible file manifest, safe filename checks, content inspection, and explicit confirmation before writing into .claude/skills/.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhengxinjipai/skills/skill-lookup-tool)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline MCP tool calls and file path instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include registry search results, selected skill metadata, file manifests, and installation confirmation.]

## Skill Version(s):

1.0.0 (source: skill.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
