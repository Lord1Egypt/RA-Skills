## Description: <br>
Automate end-to-end code implementation and testing with persistent coding and testing subagents, iterating until tests pass and committing results locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yufengwolf](https://clawhub.ai/user/yufengwolf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to coordinate small implementation-and-test workflows, split coding and testing work across persistent subagents, retry on failures, and keep local artifacts for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local code, write files, create local commits, and retain reusable subagent state. <br>
Mitigation: Use it in a clean or disposable repository, review generated diffs before accepting work, disable automatic commits where possible, and clear bundled session state before first use. <br>
Risk: Scanner review marked the release suspicious because workflow automation has limited guardrails around code execution and persisted state. <br>
Mitigation: Install only when this automation posture is acceptable, keep execution scoped to trusted workspaces, and review the generated results before relying on them. <br>


## Reference(s): <br>
- [Sample workflow specification](artifact/examples/sample_spec.txt) <br>
- [ClawHub skill page](https://clawhub.ai/yufengwolf/workflow-runner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline commands, JSON status files, shell scripts, code changes, and local result artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes workflow artifacts under results/ and may create local git commits when enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
