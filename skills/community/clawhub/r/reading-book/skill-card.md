## Description: <br>
Coordinates a book-learning workflow that extracts chapters, generates Markdown study notes, builds Neo4j Cypher, imports graph data, tracks progress, and produces a final summary report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buruqinshouburu](https://clawhub.ai/user/buruqinshouburu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to process a local book file into chapter notes, extracted concepts, Neo4j graph import batches, progress tracking, and a learning summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes embedded Neo4j credentials. <br>
Mitigation: Replace the hardcoded password before installation and use credentials scoped to a least-privilege test database. <br>
Risk: The workflow can write full book contents into local notes and graph data. <br>
Mitigation: Confirm the source material may be stored locally and review output paths before running the workflow. <br>
Risk: Generated Cypher can change a Neo4j database. <br>
Mitigation: Review generated Cypher before execution and run imports against a test database before using production data. <br>
Risk: Importer success messages may be unreliable until real writes and verification are confirmed. <br>
Mitigation: Validate database state independently after import and do not rely only on importer success messages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/buruqinshouburu/reading-book) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown notes, JSON-like structured data, Cypher statements, PowerShell commands, Python snippets, progress files, and summary reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chapter-by-chapter workflow output may include local note files and Neo4j import batches.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
