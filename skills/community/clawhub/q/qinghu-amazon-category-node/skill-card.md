## Description:

Queries Amazon category nodes by keyword, category name, path, or node ID and returns category hierarchy, names, and product counts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and researchers use this skill to find category node IDs and hierarchy, estimate category size, and supply node paths to other Amazon research tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic Node or qhkit installation and upgrades may modify the user's environment and PATH.

Mitigation: Review installation steps and use a controlled environment with a preinstalled, pinned qhkit version.

Risk: The skill may store a qhkit token and incur paid API credits.

Mitigation: Provide credentials only after reviewing where they are stored; check estimated credits and obtain consent before paid calls.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-amazon-category-node)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise Markdown answer with category paths, node IDs, product counts, and an optional table file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports credits consumed after paid calls; requires an Amazon marketplace selection.]

## Skill Version(s):

0.1.1 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
