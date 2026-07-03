## Description: <br>
围绕中药方剂、方名、来源、别名、处方、中药名、剂量、功能主治及其之间的联系构建知识谱图。仅限初步研究，具体应用需根据实际情况调整。 <br>

This skill is for research and development only. <br>

## Publisher: <br>
[cainingnk](https://clawhub.ai/user/cainingnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, developers, and traditional Chinese medicine knowledge-graph users can use this skill to inspect graph schema and run read-only Cypher queries about formulas, names, sources, aliases, prescriptions, herbs, dosages, functions, indications, and their relationships. The skill is framed as preliminary research support and should be adapted and reviewed before practical use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill collects a XiaoBenYang API key through chat and stores it in a plaintext .env file in the working directory. <br>
Mitigation: Use a limited-scope key where possible, restrict workspace access, and remove the stored key when the skill is no longer needed. <br>
Risk: Graph queries may disclose sensitive or inappropriate user-provided information to the upstream API. <br>
Mitigation: Avoid sending sensitive data in Cypher queries and review query content before execution. <br>
Risk: Copied or inconsistent documentation may make the available tools and domain boundaries unclear. <br>
Mitigation: Verify behavior against the actual tool functions exposed by the artifact before operational use. <br>


## Reference(s): <br>
- [XiaoBenYang API key portal](https://xiaobenyang.com) <br>
- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/traditional-chinese-medicine-formulas-kg) <br>
- [Publisher profile](https://clawhub.ai/user/cainingnk) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown summaries of JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns raw API results with success status and message fields; requires a XiaoBenYang API key.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
