## Description: <br>
Safely manage your AI skill collection with trust scoring, security vetting, delayed auto-updates, and pending periods for new skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liefqin](https://clawhub.ai/user/liefqin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to track installed agent skills, add new skills through a pending queue, check for updates, and apply trust-score-based update rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically change installed skills through scheduled update workflows. <br>
Mitigation: Keep cron and auto-run disabled until the operator has reviewed the registry, update rules, and each pending change. <br>
Risk: Security vetting is described by the evidence as a placeholder rather than an enforced scanner result. <br>
Mitigation: Use manual review or dry-run update checks and require real scanner results before adding or updating skills. <br>


## Reference(s): <br>
- [Skill Guardian release page](https://clawhub.ai/liefqin/skill-guardian) <br>
- [Registry format](references/registry-format.md) <br>
- [Trust rating system](references/trust-ratings.md) <br>
- [Cron setup guide](references/cron-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update a local JSON skill registry and invoke ClawHub CLI commands when its scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
