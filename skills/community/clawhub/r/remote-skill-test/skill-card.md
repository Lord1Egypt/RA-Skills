## Description: <br>
Use when the user wants to test an agent skill on a remote jump host after updating it locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panlm](https://clawhub.ai/user/panlm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to run another agent skill on a remote jump host, retrieve generated reports and logs, and compare the current run with the previous run. It supports iterative validation after local skill updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for SSH access and can run a remote agent with broad unattended authority. <br>
Mitigation: Use only isolated, non-production test hosts with least-privilege SSH accounts and test-only API keys. <br>
Risk: Retrieved reports and execution logs may contain sensitive host, prompt, or file information. <br>
Mitigation: Treat reports and opencode-run.log as sensitive and avoid shared jump hosts or environments with production credentials. <br>
Risk: The remote target, prompt, and repository source determine what the remote agent can affect. <br>
Mitigation: Review the exact prompt, target skill, remote host, and repository source before running. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/panlm/remote-skill-test) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and comparison tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces remote test status, structure-compliance analysis, report comparison, and a verdict.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
