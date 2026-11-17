## Description:

CIDR and subnet calculator for network engineers that reports IPv4 and IPv6 network details, containment checks, and subnet splitting results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, network engineers, and operations teams use this skill to calculate CIDR properties, inspect address ranges, check whether an IP belongs to a network, and split IPv4 networks into smaller subnets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad or untrusted CIDR ranges can exhaust memory or produce very large output.

Mitigation: Bound accepted network sizes and subnet split counts before using the skill in shared automation, services, or workflows that process arbitrary network input.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/johnnywang2001/skills/subnet-calc)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON subnet calculation results, with shell commands when invoking the bundled CLI script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports IPv4 and IPv6 calculations, IP containment checks, and IPv4 subnet splitting.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
