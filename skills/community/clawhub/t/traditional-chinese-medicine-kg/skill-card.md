## Description:

围绕中药名，中药材，别名，来源，分布，功能，主治，归经，四气，四气及其之间的联系构建知识谱图。仅限初步研究，具体应用需根据实际情况调整。

This skill is for research and development only.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, developers, and external users can query a Traditional Chinese Medicine knowledge graph for herb names, aliases, sources, distributions, functions, indications, meridians, qi properties, and their relationships. The skill is intended for preliminary research support, with practical application decisions requiring user review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends graph queries and an API key to a remote XiaoBenYang service.

Mitigation: Install and use the skill only when the XiaoBenYang service is trusted for the intended data and access scope.

Risk: The skill can store the XiaoBenYang API key in a plaintext .env file in the working directory.

Mitigation: Use a scoped or disposable key where possible, keep .env out of backups and source control, and rotate the key if exposure is suspected.

Risk: Copied gaokao and school-search references may confuse users about the skill's actual Traditional Chinese Medicine knowledge-graph purpose.

Mitigation: Review the skill before routine use and have the publisher correct stale copied references.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/traditional-chinese-medicine-kg)
- [cainingnk ClawHub profile](https://clawhub.ai/user/cainingnk)
- [XiaoBenYang API key portal](https://xiaobenyang.com)
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or text summaries derived from JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key and supports schema lookup plus read-only Cypher queries.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
