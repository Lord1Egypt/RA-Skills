## Description: <br>
Analyze Sui Move test coverage, identify untested code, write missing tests, and perform security audits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EasonC13](https://clawhub.ai/user/EasonC13) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to inspect Sui Move test coverage, identify untested functions, branches, and assertions, generate missing tests, and document security review findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs the agent to commit generated test changes automatically. <br>
Mitigation: Use the skill on a branch, review coverage reports and test diffs, and approve any git commit only after inspecting the changes. <br>
Risk: Generated tests or security recommendations may be incomplete or incorrect for the target Sui Move contract. <br>
Mitigation: Run the Sui test and coverage commands after changes, review the generated report, and validate security findings against the contract's intended behavior. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/EasonC13/sui-auto-test) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown reports, Move test code, JSON or Markdown coverage summaries, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write coverage reports and test changes in a local Sui Move project.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
