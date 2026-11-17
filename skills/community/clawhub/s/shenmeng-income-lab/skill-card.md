## Description:

Income Lab helps users design, track, review, and improve income experiments across legal earning methods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenmeng](https://clawhub.ai/user/shenmeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to assess their time, skills, capital, and risk tolerance; choose income experiments; track income and hours; and decide which strategies to continue, adjust, or stop.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic external charging is part of the packaged billing flow.

Mitigation: Install only after confirming the 0.01 USDT per-call model, the billing provider, and the user identity used for charges.

Risk: A reusable payment API key appears in source.

Mitigation: Require key rotation or environment-based secret handling before trusted deployment.

Risk: The bundled scripts can store income experiment records locally.

Mitigation: Avoid entering sensitive financial details unless local storage under ~/.income-lab is acceptable.

## Reference(s):

- [Income Methods Reference](references/income-methods.md)
- [Retrospective Framework](references/retrospective-framework.md)
- [ClawHub Skill Page](https://clawhub.ai/shenmeng/skills/shenmeng-income-lab)
- [Publisher Profile](https://clawhub.ai/user/shenmeng)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with command examples; bundled scripts can write JSON records and CSV reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local income experiment records under ~/.income-lab when the bundled scripts are run.]

## Skill Version(s):

2025.4.15 (source: server release evidence; artifact _meta.json lists 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
