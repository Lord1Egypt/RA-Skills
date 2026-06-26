## Description: <br>
AI-powered knowledge management intelligence. Search taxonomies, content curation records, expertise directories, and communities of practice with structured extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RooJenkins](https://clawhub.ai/user/RooJenkins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Knowledge management practitioners, content stewards, and organizational leaders use this skill to search and reason over taxonomies, expertise directories, communities of practice, content lifecycle records, and knowledge gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose broad organizational context through search and full-context export workflows. <br>
Mitigation: Use a scoped UPLO token, prefer targeted searches over full exports, and require explicit confirmation before exporting organizational context. <br>
Risk: Knowledge gap reports, outdated-content flags, and update proposals may affect knowledge records or route inaccurate guidance to owners. <br>
Mitigation: Require human review, audit logging, and rollback or correction workflows before relying on record-changing actions. <br>
Risk: Expertise, succession planning, and knowledge audit data may include confidential or restricted information. <br>
Mitigation: Enforce classification tiers and access controls before surfacing sensitive knowledge-management results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RooJenkins/uplo-knowledge-management) <br>
- [UPLO](https://uplo.ai) <br>
- [UPLO schemas](https://uplo.ai/schemas) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with MCP tool calls, query examples, and knowledge-management findings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require an UPLO instance URL and a scoped UPLO MCP token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
