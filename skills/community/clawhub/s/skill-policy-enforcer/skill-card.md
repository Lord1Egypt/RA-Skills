## Description: <br>
Use when checking an agent Skill against a local or enterprise policy before installation, publication, CI approval, marketplace review, or repository merge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[debtvc2022](https://clawhub.ai/user/debtvc2022) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, platform teams, and marketplace reviewers use this skill to run repeatable policy checks over agent Skill folders before installation, publication, CI approval, marketplace review, or repository merge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The policy checker reads files under the folder it is asked to scan, which could include unrelated private data if pointed at a broad directory. <br>
Mitigation: Run it against the intended skill folder or another deliberately scoped directory, and avoid broad directories containing unrelated private data unless that scan is intentional. <br>
Risk: Policy findings can block installation, release, CI, marketplace review, or repository merge workflows. <br>
Mitigation: Use an explicit local policy file for approved exceptions and review deny or warn results by their reported rule IDs. <br>


## Reference(s): <br>
- [Policy schema](references/policy-schema.md) <br>
- [Default policy](references/default-policy.yaml) <br>
- [ClawHub release page](https://clawhub.ai/debtvc2022/skill-policy-enforcer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON policy-check results with rule IDs and pass/fail/warning status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can apply a caller-supplied JSON or simple YAML policy, or the bundled default conservative policy.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
