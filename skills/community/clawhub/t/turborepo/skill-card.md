## Description:

Provides guidance for configuring and optimizing Turborepo monorepos, including task pipelines, package structure, caching, filtering, CI, and environment variables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to set up, troubleshoot, and optimize JavaScript and TypeScript monorepos that use Turborepo. It helps agents propose turbo.json task configuration, package scripts, cache behavior, filtering commands, CI workflows, and environment variable handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation guidance includes a mutable GitHub main-branch path that can change after review.

Mitigation: Install from a pinned, reviewed ClawHub version or an immutable commit rather than a mutable branch.

Risk: CI remote-cache examples can expose broad TURBO_TOKEN access if copied without adjustment.

Mitigation: Scope TURBO_TOKEN only to the build or test steps that need remote caching and use a narrowly scoped token.

Risk: Generated build, cache, and CI changes can affect monorepo execution behavior across many packages.

Mitigation: Review proposed configuration changes and run representative build, test, cache, and affected-package checks before merging.

## Reference(s):

- [ClawHub Turborepo Skill Page](https://clawhub.ai/wpank/skills/turborepo)
- [Turborepo Documentation](https://turborepo.dev/docs)
- [Turborepo Run Reference](https://turborepo.dev/docs/reference/run)
- [Turborepo Configuration Reference](https://turborepo.dev/docs/reference/configuration)
- [Turborepo Remote Caching](https://turborepo.dev/docs/core-concepts/remote-caching)
- [Turborepo Source Documentation Index](artifact/SKILL.md#source-documentation)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include turbo.json snippets, package.json scripts, CI workflow fragments, and troubleshooting checklists.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 2.7.6)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
