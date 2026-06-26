## Description: <br>
Predicts code change impact by analyzing knowledge graph call chains to identify directly and indirectly affected modules before commit, merge, or review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sipoon](https://clawhub.ai/user/sipoon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect git diffs against a local code knowledge graph, estimate direct and chained impact, and identify areas that need extra review before commit or merge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect git diffs and use or create a local code knowledge graph. <br>
Mitigation: Use it only in repositories where local indexing and diff inspection are acceptable. <br>
Risk: Dynamic calls, reflection, dependency injection, or very deep dependency chains may be missed or truncated. <br>
Mitigation: Treat the report as review guidance and validate high-risk areas with tests or human review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sipoon/sipoon-diff-impact) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown impact report with dependency layers, risk areas, and optional shell command suggestions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses repository diffs and a local knowledge graph; large or highly dynamic code paths may be incomplete.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
