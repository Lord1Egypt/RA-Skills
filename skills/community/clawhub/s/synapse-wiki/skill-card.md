## Description: <br>
Synapse Wiki builds and maintains a persistent local knowledge base by ingesting source materials, creating structured wiki pages, answering queries, and checking wiki health. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ankechenlab-node](https://clawhub.ai/user/ankechenlab-node) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge workers, and documentation maintainers use this skill to create a local wiki, ingest raw notes or articles, query accumulated knowledge, and inspect wiki link health. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently writes wiki summaries, indexes, logs, and query outputs to local paths selected by the user. <br>
Mitigation: Use a dedicated wiki folder and review generated files before sharing or syncing them. <br>
Risk: Raw materials may contain secrets or private project information that become summarized or logged in the local wiki. <br>
Mitigation: Avoid placing secrets in raw sources and review generated pages before publication or team distribution. <br>
Risk: Automatic synapse-code/wiki logging can preserve technical decisions and project context that may not be appropriate for every repository. <br>
Mitigation: Enable automatic logging only for projects where persistent documentation of development decisions is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ankechenlab-node/synapse-wiki) <br>
- [Publisher profile](https://clawhub.ai/user/ankechenlab-node) <br>
- [Project homepage](https://github.com/ankechenlab-node/synapse-wiki) <br>
- [Karpathy LLM Wiki reference](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, terminal text, wiki files, and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local wiki directories, summary pages, index files, logs, and query output files under user-selected paths.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
