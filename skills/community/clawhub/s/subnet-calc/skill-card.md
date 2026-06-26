## Description: <br>
CIDR and subnet calculator for network engineers. Calculate network address, broadcast, host range, subnet mask, wildcard mask, and more from CIDR notation. Supports IPv4 and IPv6, containment checks, and subnet splitting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnywang2001](https://clawhub.ai/user/Johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network engineers, developers, and operators use this skill to calculate CIDR subnet details, check whether an IP address belongs to a network, and split IPv4 networks into smaller subnets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Extremely large subnet calculations or split operations can consume high local CPU or memory. <br>
Mitigation: Use bounded CIDR ranges and split prefixes appropriate for the machine running the tool; avoid expanding very large address spaces unless resource use is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Johnnywang2001/subnet-calc) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON CLI output, with Markdown guidance when used by an agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local Python standard-library execution; no credentials or network access required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
