## Description: <br>
Reckit helps agents verify, audit, build, rebuild, and fix code by running multi-gate checks such as slop scans, type checks, mutation tests, cross-verification, security scans, and proof bundle generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[christiancattaneo](https://clawhub.ai/user/christiancattaneo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use Reckit to run structured verification on software projects before shipping changes. It supports greenfield builds, rebuilds, bug fixes, and audits with gate results and Ship, Caution, or Blocked verdicts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute project code and tooling while auditing or verifying a repository. <br>
Mitigation: Run it in a sandbox or disposable worktree for untrusted projects and review commands before executing gates. <br>
Risk: The skill can write files, mutate code, spawn workers, and sometimes commit changes with weak consent boundaries. <br>
Mitigation: Keep approval controls enabled, use audit-only mode when changes are not desired, and review generated changes and proof bundles before accepting results. <br>
Risk: Dashboard and sandbox-bypass guidance may increase local exposure or privilege risk. <br>
Mitigation: Avoid the dashboard or sandbox-bypass workflow unless the local exposure and privilege implications are understood. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/christiancattaneo/wreckit-ralph) <br>
- [Verification framework](references/verification-framework.md) <br>
- [Swarm orchestrator](references/swarm/orchestrator.md) <br>
- [Worker handoff](references/swarm/handoff.md) <br>
- [Slop scan gate](references/gates/slop-scan.md) <br>
- [Type check gate](references/gates/type-check.md) <br>
- [Mutation kill gate](references/gates/mutation-kill.md) <br>
- [Cross-verify gate](references/gates/cross-verify.md) <br>
- [SAST gate](references/gates/sast.md) <br>
- [Proof bundle gate](references/gates/proof-bundle.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON gate outputs, generated configuration, and proof bundle files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write .wreckit proof artifacts and repository files when gates or build/fix modes require changes.] <br>

## Skill Version(s): <br>
2.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
