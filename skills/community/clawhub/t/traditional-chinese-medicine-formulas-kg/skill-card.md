## Description:

围绕中药方剂、方名、来源、别名、处方、中药名、剂量、功能主治及其之间的联系构建知识谱图。仅限初步研究，具体应用需根据实际情况调整。

This skill is for research and development only.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and agents use this skill to inspect a traditional Chinese medicine formula knowledge graph, fetch graph schema details, and execute read-only Cypher queries for preliminary research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the XiaoBenYang API key in a local plaintext .env file.

Mitigation: Use a limited-scope key when possible, keep .env out of source control and backups, avoid shared workspaces, and rotate the key if exposure is suspected.

Risk: The release security verdict is suspicious because API-key storage has weak disclosure and controls.

Mitigation: Install only after accepting that storage behavior and review local secret-handling practices before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/traditional-chinese-medicine-formulas-kg)
- [Publisher profile](https://clawhub.ai/user/cainingnk)
- [XiaoBenYang API key provider](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, API results, guidance]

**Output Format:** [Markdown summary of JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key and returns schema data or read-only Cypher query results.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
