## Description: <br>
Run high-signal autonomous coding loops with Soulforge (feature-dev/bugfix/review-loop) using strict worktree isolation, review gates, and scoped fix cycles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jamesrp13](https://clawhub.ai/user/jamesrp13) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering operators use this skill to run Soulforge feature-development, bugfix, and review-loop workflows in isolated worktrees with scoped tasks, review gates, and callback-based status handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides powerful local coding workflows and GitHub CLI usage in trusted repositories. <br>
Mitigation: Install only when the local soulforge and gh binaries are trusted, run workflows in dedicated worktrees, keep tasks narrow, and confirm GitHub authentication targets the intended account and repository. <br>
Risk: Callback execution can run operator-selected delivery commands. <br>
Mitigation: Review callback commands before launch, pass workflow-produced callback messages through unchanged where possible, and avoid embedding untrusted task text or variables into shell fragments. <br>


## Reference(s): <br>
- [Workflow YAML Format](references/workflow-format.md) <br>
- [Soulforge ClawHub Skill Page](https://clawhub.ai/jamesrp13/soulforge) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires trusted local soulforge and gh binaries; produces operator-facing workflow guidance rather than executable artifacts.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
