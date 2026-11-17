## Description:

Helps calculate the rate at which trust in a skill or agent is decaying by combining time elapsed since last verification with the rate of change in behavior, permissions, or dependencies, producing a trust velocity score that predicts when a trusted credential will become unreliable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud)

### License/Terms of Use:


## Use Case:

Developers, security reviewers, and agent platform operators use this skill to estimate how quickly a skill or agent's trust posture decays after verification as time passes and behavior, permission, endpoint, dependency, or instruction changes accumulate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The visible artifact describes a methodology and report format rather than a complete implemented calculator, while the metadata declares curl and python3 requirements.

Mitigation: Review future versions before installation if executable helpers, network calls, or automated data collection are added.

Risk: A high trust velocity score can be misread as evidence that a skill is malicious or compromised.

Mitigation: Treat the score as a re-verification and review-prioritization signal, and corroborate it with security review before making enforcement decisions.

Risk: Version histories with frequent superficial releases may inflate change velocity without reflecting meaningful risk.

Mitigation: Calibrate decay parameters to the operating environment and inspect the substance of changes before acting on threshold alerts.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown trust velocity report with scores, projections, change breakdowns, urgency labels, and recommended actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory trust assessments and projections rather than proof of compromise.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
