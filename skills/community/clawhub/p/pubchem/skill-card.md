## Description:

该服务通过PubChem API提取药物基础化学信息，包括分子式、分子量、CAS号等关键数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers can use this skill to look up chemical substance details by name or CAS number and present the returned chemistry data to a user. Use requires a Xiaobenyang API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence says the skill claims PubChem chemistry lookup but routes queries and the persisted API key through a Xiaobenyang MCP client with unclear boundaries.

Mitigation: Install only if the user intends to trust Xiaobenyang with the API key and chemical queries; verify the service boundary before use.

Risk: The skill stores the Xiaobenyang API key in a plaintext .env file.

Mitigation: Use a low-privilege API key, avoid valuable credentials, and remove or rotate the key after use.

Risk: The security guidance recommends avoiding valuable credentials until the publisher addresses the PubChem/Xiaobenyang mismatch, plaintext persistence, endpoint validation, and callable API surface.

Mitigation: Review the skill before installing and defer sensitive use until the publisher documents or narrows these behaviors.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/pubchem)
- [Xiaobenyang API key site](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown summary of JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns success status, raw upstream response data, and a status message.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
