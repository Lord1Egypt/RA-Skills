## Description:

Provides Composer Kit React component documentation, examples, props, installation guidance, and Celo Composer CLI information for developers building Celo web3 applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building Celo web3 applications use this skill to look up Composer Kit components, usage examples, prop details, installation instructions, component categories, and Celo Composer CLI create-command guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an XBY API key and sends documentation queries plus the key to the XiaoBenYang backend.

Mitigation: Install only if the XiaoBenYang service is trusted, use scoped credentials when available, and avoid sending sensitive project details in queries.

Risk: The skill persists the XBY API key in a local .env file.

Mitigation: Treat the .env file as secret material, keep it out of source control and shared workspaces, and restrict file permissions.

Risk: The release evidence recommends clearer disclosure and pinned dependencies before broader use.

Mitigation: Review the skill before deployment and pin dependencies in controlled environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/react-composer-kit)
- [ALinkLab publisher profile](https://clawhub.ai/user/alinklab)
- [XiaoBenYang service](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown summaries with code examples and JSON-derived documentation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY API key and sends documentation queries to the XiaoBenYang service.]

## Skill Version(s):

1.0.1 (source: release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
