## Description: <br>
Transform natural language questions into SPARQL queries for DBpedia and generate result outputs as JSON, Markdown, or HTML. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kidehen](https://clawhub.ai/user/kidehen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and analysts use this skill to turn plain-English questions about DBpedia entities into SPARQL queries, execute them against DBpedia, and format results for inspection or sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Questions and generated SPARQL queries may be sent to the public DBpedia endpoint. <br>
Mitigation: Use the skill for public research and avoid confidential, sensitive, or proprietary information in prompts. <br>
Risk: Requested HTML report generation can create local files. <br>
Mitigation: Review the intended output path and generated HTML contents before sharing or publishing reports. <br>
Risk: DBpedia data may be incomplete, stale, or different from current real-world facts. <br>
Mitigation: Treat results as structured DBpedia data and verify important facts against authoritative sources when accuracy matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kidehen/query-dbpedia) <br>
- [DBpedia SPARQL endpoint](https://dbpedia.org/sparql) <br>
- [DBpedia homepage](https://dbpedia.org) <br>
- [DBpedia documentation](https://www.dbpedia.org/resources/documentation/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands] <br>
**Output Format:** [JSON results, Markdown tables, SPARQL code, shell commands, or generated HTML files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute HTTP GET requests against the DBpedia SPARQL endpoint and may save local HTML reports when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and README) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
