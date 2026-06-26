## Description: <br>
Answer questions from a persistent markdown knowledge wiki and file durable results back into the wiki when useful. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teki-ai](https://clawhub.ai/user/teki-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and team knowledge maintainers use this skill to answer questions against an existing markdown wiki, synthesize across related pages, cite wiki evidence, and save durable analysis pages when the result is worth reusing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create or update persistent wiki files, including analysis pages, index entries, and query logs. <br>
Mitigation: Use it only in workspaces where those writes are acceptable, then review diffs before committing or sharing the wiki. <br>
Risk: Private or sensitive material supplied to the wiki could be preserved in durable markdown outputs. <br>
Mitigation: Avoid providing secrets or private material unless that content belongs in the wiki. <br>
Risk: Synthesis across wiki pages can produce misleading conclusions when source evidence is incomplete or conflicting. <br>
Mitigation: Require citations, separate direct support from synthesis, and surface uncertainty or disagreement in the answer. <br>


## Reference(s): <br>
- [Query Patterns](references/query-patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/teki-ai/wiki-query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown answers with wiki citations and optional markdown file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update reusable analysis pages, index entries, and query log entries when the result has durable value.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
