## Description: <br>
Helps users discover suitable skills, recommend skill combinations by task type, and receive guided usage instructions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pagoda111king](https://clawhub.ai/user/pagoda111king) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to search for relevant ClawHub skills, choose task-oriented skill combinations, and generate basic usage guidance for unfamiliar skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan flags the release as suspicious because requested Write, Bash, and Exec permissions are broader than the visible helper behavior justifies. <br>
Mitigation: Review before installing, prefer a least-privilege version, and require explicit user approval before file writes or command execution. <br>
Risk: The artifact advertises vector search and automatic optimization, while the implementation uses simple keyword and rule-based matching. <br>
Mitigation: Treat recommendations as advisory, manually validate selected skills, and avoid relying on claimed semantic ranking until implemented evidence is provided. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pagoda111king/skill-discoverer-pro) <br>
- [Skill Discoverer documentation](https://docs.cloud-shrimp.com/skill-discoverer) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown, Code] <br>
**Output Format:** [Markdown and structured JavaScript objects describing search results, recommendations, combinations, and usage guides] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations are based on simple keyword and rule-based matching in the submitted artifact.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata, SKILL.md frontmatter, and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
