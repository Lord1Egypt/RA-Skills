## Description: <br>
围绕中药名，中药材，别名，来源，分布，功能，主治，归经，四气，四气及其之间的联系构建知识谱图。仅限初步研究，具体应用需根据实际情况调整。 <br>

This skill is for research and development only. <br>

## Publisher: <br>
[cainingnk](https://clawhub.ai/user/cainingnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill for preliminary exploration of a traditional Chinese medicine knowledge graph, including graph schema inspection and read-only Cypher queries over medicine names, materials, aliases, sources, distributions, functions, indications, meridians, and four-nature relationships. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists the user-provided XBY_APIKEY in a local plaintext .env file. <br>
Mitigation: Use a scoped or disposable API key and run the skill only in directories where a local plaintext .env file is acceptable. <br>
Risk: Graph queries and parameters are sent to a remote XiaoBenYang service. <br>
Mitigation: Avoid submitting sensitive graph queries or confidential data unless the remote provider and API terms are acceptable. <br>
Risk: Server security evidence flags mismatched documentation and broad remote query behavior. <br>
Mitigation: Review the artifact, requested query, and remote API behavior before deployment or operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/traditional-chinese-medicine-kg) <br>
- [Publisher profile](https://clawhub.ai/user/cainingnk) <br>
- [XiaoBenYang API key portal](https://xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, configuration, guidance] <br>
**Output Format:** [Markdown summaries of JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an XBY_APIKEY before querying the remote graph service; query results depend on the upstream API response.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
