## Description: <br>
AI-powered GitHub knowledge management. Search repository metadata, code review standards, issue tracking, and team workflows with structured extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RooJenkins](https://clawhub.ai/user/RooJenkins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to search organization-specific GitHub repository metadata, ownership records, pull request and issue history, review standards, and workflow guidance through a configured UPLO knowledge base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured UPLO instance may expose sensitive organizational GitHub metadata, discussions, repository ownership, and team context. <br>
Mitigation: Install only for trusted UPLO instances, use least-privilege MCP tokens, and keep access aligned with organizational classification tiers. <br>
Risk: The export_org_context tool may return broad internal repository and team context. <br>
Mitigation: Limit use of broad exports, review outputs before sharing, and avoid surfacing credentials or deployment secrets. <br>
Risk: Indexed GitHub data is a snapshot and may be stale for current CI status, latest commits, or recently changed ownership. <br>
Mitigation: Confirm time-sensitive repository state directly in GitHub before acting on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RooJenkins/uplo-github) <br>
- [UPLO](https://uplo.ai) <br>
- [UPLO schemas](https://uplo.ai/schemas) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline tool calls and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return organization-specific GitHub context from the configured UPLO MCP instance; users should confirm time-sensitive GitHub state in GitHub directly.] <br>

## Skill Version(s): <br>
1.0.0 (source: skill.json and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
