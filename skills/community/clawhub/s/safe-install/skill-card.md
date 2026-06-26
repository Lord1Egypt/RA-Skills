## Description: <br>
Install OpenClaw skills through policy validation, ClawShield scanning, snapshot storage, and rollback controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mike007jd](https://clawhub.ai/user/mike007jd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Safe Install to review, scan, install, track, and roll back locally managed OpenClaw skills under a policy-controlled workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using --force can install skills classified as Avoid. <br>
Mitigation: Reserve --force for reviewed cases and keep forceRequiredForAvoid enabled in policy unless there is a documented exception. <br>
Risk: The avoid-skill fixture contains a risky shell sample. <br>
Mitigation: Treat fixture files as test evidence only and do not run the avoid-skill fixture script manually. <br>
Risk: A weak or stale policy can allow sources or patterns that the user did not intend to trust. <br>
Mitigation: Review the policy file before installation and use policy validate to check policy structure. <br>


## Reference(s): <br>
- [ClawHub Safe Install release page](https://clawhub.ai/mike007jd/safe-install) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text or JSON envelopes, with Markdown command examples in the skill instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Installation history, rollback state, policy validation results, and scan-driven install decisions may be emitted by the CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
