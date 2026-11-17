## Description:

Build or convert Art Blocks generative art scripts using artblocks-mcp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryley-o](https://clawhub.ai/user/ryley-o)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and generative artists use this skill to scaffold new Art Blocks projects or convert existing artwork into the Art Blocks generator format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated starter code or conversion guidance may include mistakes that affect determinism, rendering, or Art Blocks compatibility.

Mitigation: Review generated code and verify deterministic initial renders with the same tokenData hash before publishing artwork.

Risk: External asset stubs such as IPFS or Arweave references may point to unavailable or unintended content if left unreviewed.

Mitigation: Inspect and replace external asset references before release, and confirm each dependency matches the intended artwork.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryley-o/skills/scaffold-art-script)
- [Art Blocks generator spec](artblocks://generator-spec)

## Skill Output:

**Output Type(s):** [Guidance, Code, Files, Configuration instructions]

**Output Format:** [Markdown guidance plus generated HTML and JavaScript project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include p5.js, Three.js, vanilla JavaScript, PostParams, FLEX dependency stubs, and window.$features trait stubs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
