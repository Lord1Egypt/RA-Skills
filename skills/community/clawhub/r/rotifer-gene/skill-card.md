## Description:

Guides developers through creating, testing, auditing, publishing, and migrating Rotifer Genes with the Rotifer CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoba-dev](https://clawhub.ai/user/xiaoba-dev)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers use this skill to build and test Rotifer Genes, audit them for exposed credentials and unsafe artifacts, publish them to the Rotifer Registry, and migrate their fidelity between Wrapped, Hybrid, and Native.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports a benign verdict with medium confidence, but the scan covered only five of six components and partly inspected migration material.

Mitigation: Review the complete release, including the migration material, and perform the documented audit before installing or publishing Genes.

Risk: The security guidance calls out external-request examples, and the documented CLI can run Hybrid or Wrapped Gene code that makes network requests.

Mitigation: Review each request destination and the data it sends; keep Hybrid Gene hosts restricted to the declared allowedDomains before running the code.

Risk: Publishing uploads Gene metadata, phenotype data, README content, changelog, and compiled WASM to Rotifer Cloud, where the release is public; the wrap command may offer to publish when Enter is pressed.

Mitigation: Run the four-layer audit and inspect all publishable files before publishing; disable default publishing if the prompt could be accepted unintentionally.

## Reference(s):

- [Gene Development](modules/dev.md)
- [Gene Security Audit](modules/audit.md)
- [Gene Fidelity Migration](modules/migration.md)
- [Rotifer Protocol](https://rotifer.dev)
- [Rotifer Documentation](https://rotifer.dev/docs)
- [Rotifer Protocol Specification](https://github.com/rotifer-protocol/rotifer-spec)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with TypeScript and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reference material is organized into on-demand development, audit, and migration modules.]

## Skill Version(s):

1.0.12 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
