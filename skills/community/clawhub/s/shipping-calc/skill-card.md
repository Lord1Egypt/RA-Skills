## Description:

Calculate shipping costs with zone-based rates and duty estimates. Use when estimating shipping costs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations users can ask an agent to estimate shipping rates, compare standard and express costs, estimate billable dimensional weight, and calculate simple duty estimates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted shipping values can make the shell script run arbitrary local commands.

Mitigation: Review the skill before installing, avoid untrusted shipment values, and require fixed awk argument handling with validated numeric inputs before routine use.

Risk: Shipping outputs may be misleading because pricing is not actually zone-based and the track and batch commands are placeholders.

Mitigation: Clarify the calculator's limitations, document local data use, and verify rates, duties, tracking, and batch workflows against authoritative shipping sources before relying on results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/shipping-calc)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text command output with Markdown command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local shipping, dimensional weight, duty, tracking, and batch-processing command outputs.]

## Skill Version(s):

3.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
