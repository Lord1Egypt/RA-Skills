## Description:

Generates adversarial probes from known attack templates, evaluates a target policy against red-team ground truth, and reports robustness, blind spots, and over-refusals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and safety engineers use this skill to generate adversarial probes, run policy robustness checks before or after deployment, and identify policy blind spots for follow-up hardening.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local learning records may retain prompts, notes, preferences, or policy evaluation context across sessions.

Mitigation: Avoid storing secrets or sensitive prompts in learner notes or preferences, and periodically inspect or delete learned_patterns.json when retention matters.

Risk: Custom policy loading imports local modules supplied by the user.

Mitigation: Load only trusted local policy modules and review policy code before running evaluations.

Risk: Known attack templates do not cover all unknown or novel jailbreak techniques.

Mitigation: Treat results as regression and coverage signals, and supplement them with broader adversarial testing for high-impact deployments.

Risk: Incorrect red-team ground-truth labels can skew robustness scores and blind spot reporting.

Mitigation: Review labels for representative payloads and manually verify high-impact findings before using the score as a release gate.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and JSON evaluation output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces robustness scores, flip counts, over-refusal counts, and blind spot lists from local policy evaluation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
