## Description:

Generate, revise, validate, and render official WaveDrom diagrams from natural-language timing descriptions, protocol requirements, timing tables, or existing WaveJSON/JSON5.

This skill is ready for commercial/non-commercial use.

## Publisher:

[siliconpeasant](https://clawhub.ai/user/siliconpeasant)

### License/Terms of Use:

MIT

## Use Case:

Developers and hardware engineers use this skill to convert timing descriptions, protocol requirements, timing tables, or existing WaveJSON into editable WaveJSON/JSON5 and rendered WaveDrom diagrams. It is suited for digital timing diagrams, protocol handshakes, register and logic diagrams, and optional datasheet-style timing annotations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes generated diagram artifacts to local paths and can overwrite files when overwrite behavior is explicitly enabled.

Mitigation: Review destination paths before rendering and use overwrite only intentionally.

Risk: MCP registration is a persistent agent configuration change separate from installing the skill.

Mitigation: Use dry-run registration when reviewing the change and replace existing registrations only with explicit intent.

Risk: Unpinned external CLI execution can produce renderer behavior that differs from the bundled skill baseline.

Mitigation: Prefer the bundled Node scripts or MCP tools that use the pinned wavedrom 3.6.2 dependency.

Risk: A renderable diagram may still be semantically wrong for a protocol or timing contract.

Mitigation: Review assumptions, active edges, latency, signal polarity, and protocol-specific transfer rules before relying on the diagram.

## Reference(s):

- [Official WaveJSON reference](references/wavejson-official.md)
- [Protocol clarification and defaults](references/protocol-questions.md)
- [Timing semantic review](references/semantic-review.md)
- [Datasheet annotations](references/datasheet-annotations.md)
- [MCP tools](references/mcp-tools.md)
- [MCP registration](references/mcp-registration.md)
- [WaveDrom repository](https://github.com/wavedrom/wavedrom)
- [WaveDrom tutorial](https://wavedrom.com/tutorial.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with artifact paths, editable WaveJSON/JSON5 source, SVG files, and optional PNG or self-contained HTML.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 20 or newer; renders with pinned wavedrom 3.6.2 and optional @resvg/resvg-js PNG conversion.]

## Skill Version(s):

0.3.1 (source: frontmatter and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
