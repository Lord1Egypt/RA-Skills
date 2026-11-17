## Description:

Convert Chinese or English natural-language requests for an OpenClaw-powered omnidirectional smart cart into conservative, structured motion plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason15336804](https://clawhub.ai/user/jason15336804)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and robotics operators use this skill to translate bilingual smart-cart movement requests into conservative JSON control plans with explicit assumptions, sensing steps, final stops, and confirmation requirements for ambiguous or high-risk motion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated plans may be unsafe if treated as proof that sensing or obstacle checks occurred.

Mitigation: Require independent controller-side safety enforcement and real sensor validation before any physical cart movement.

Risk: The bundled validator can approve movement plans that omit required sensing checks.

Mitigation: Review plans manually for required sensing behavior and fix or supplement validation before connecting outputs to hardware.

Risk: The skill can propose motion for ambiguous destinations, people nearby, or unclear routes.

Mitigation: Use needs_confirmation for ambiguous or high-risk requests and keep speeds conservative near obstacles, people, turns, and narrow areas.

## Reference(s):

- [Command plan schema](references/command-schema.md)
- [Sample smart-cart plan](examples/sample-plan.json)
- [ClawHub skill page](https://clawhub.ai/jason15336804/skills/smart-cart-command-planner)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Shell commands, Guidance]

**Output Format:** [JSON object followed by a short human-readable explanation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plans should preserve the original request, normalize distances and angles, include ordered executable steps, record assumptions, and be validated with the bundled Python validator when file execution is available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
