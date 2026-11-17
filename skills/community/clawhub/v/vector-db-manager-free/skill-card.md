## Description: <br>
This skill helps AI application developers manage vector database indexes, embeddings, similarity search, collections, partitions, and basic performance tuning across local and cloud deployments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to operate vector database workflows for semantic search, recommendations, and retrieval-backed applications. It is intended for creating indexes, importing embeddings, running KNN or ANN similarity searches, and checking basic database statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents through database-changing operations such as delete, rebuild, overwrite, import, or export actions. <br>
Mitigation: Require explicit target database details and manual confirmation before any destructive or state-changing operation. <br>
Risk: Using the skill against production databases with broad credentials could modify or expose real data. <br>
Mitigation: Start with read-only or test credentials and review the skill before installing it in environments with real databases. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/vector-db-manager-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with SQL, Python, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce database operation plans, structured status responses, execution logs, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
