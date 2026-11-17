## Description:

Methods for teaching physical and embodied skills to others, including hands-on activities such as riding a bike, swimming, cooking, driving, using tools, and other skills that require physical demonstration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, coaches, parents, instructors, and caregivers use this skill to plan and explain how to teach physical skills with demonstration, practice, feedback, readiness checks, and safety-aware progression.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release asks for filesystem access that the security evidence describes as unnecessary.

Mitigation: Install with least privilege and avoid granting filesystem access unless the publisher explains why it is needed.

Risk: The release evidence flags an unpinned npx install command.

Mitigation: Use a trusted ClawHub installation path and pin the CLI or package version where possible.

Risk: The skill covers physical activities with real safety exposure, including swimming, driving, knives, and tools.

Mitigation: Treat the skill as planning guidance and use qualified supervision, protective equipment, and applicable local safety or legal requirements.

## Reference(s):

- [Schmidt and Lee, Motor Control and Learning](https://us.humankinetics.com/)
- [American Montessori Society](https://amshq.org/)
- [American Red Cross Learn-to-Swim](https://www.redcross.org/take-a-class/swimming)
- [National Highway Traffic Safety Administration](https://www.nhtsa.gov/)
- [Anthropic Labor Market Impacts of AI](https://www.anthropic.com/research/labor-market-impacts)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with structured checklists, step-by-step protocols, and state-tracking configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include safety-oriented recommendations for qualified supervision, protective equipment, and local legal requirements.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
