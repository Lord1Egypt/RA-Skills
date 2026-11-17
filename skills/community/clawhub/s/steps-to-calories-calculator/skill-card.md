## Description:

Calculates calories burned walking from body weight and step count, using a peer-reviewed biomechanics formula (Weyand, Smith, Puyau & Butte, 2010, Journal of Experimental Biology) rather than a generic guess.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arbazex](https://clawhub.ai/user/arbazex)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to estimate net calories burned from walking after providing body weight and step count. The skill is intended for general fitness curiosity and explains the assumptions, calculation, and reliability limits of the estimate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles body weight and step count, which may feel personal to users.

Mitigation: The artifact is self-contained and does not store or transmit these inputs; avoid asking for unnecessary additional health information.

Risk: Users could mistake a walking calorie estimate for medical, clinical, or weight-management advice.

Mitigation: Present results as approximate general fitness estimates and direct users to a doctor or registered dietitian for clinical or weight-management decisions.

Risk: The formula is less reliable for running, stairs, steep inclines, loaded walking, uneven terrain, or atypical gait patterns.

Mitigation: Ask for context when useful and clearly flag lower confidence when the walk falls outside level, normal walking conditions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arbazex/skills/steps-to-calories-calculator)
- [Server-resolved source repository](https://github.com/arbazex/steps-to-calories-calculator)
- [Weyand et al. 2010 DOI](https://doi.org/10.1242/jeb.048199)
- [Weyand et al. 2010 open access article](https://journals.biologists.com/jeb/article/213/23/3972/10061/)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown with arithmetic steps and plain-language caveats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a single walking calorie estimate after collecting body weight and step count; does not store or transmit user inputs.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
