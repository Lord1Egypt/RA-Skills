## Description: <br>
TuleBank lets an agent check wallet balance, send ARS to CVU or ALIAS destinations, swap USDC and wARS, manage beneficiaries, and move funds through ARS off-ramp and on-ramp flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aromeoes](https://clawhub.ai/user/aromeoes) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and their agents use TuleBank to operate Ripio/tulebank wallet workflows, including balance checks, beneficiary management, ARS transfers to CVU or ALIAS recipients, USDC/wARS swaps, and ARS on-ramp or off-ramp flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This skill can initiate real-money financial transfers, swaps, and ARS on-ramp or off-ramp flows. <br>
Mitigation: Verify the publisher and binary source, confirm every amount, recipient, destination, and swap detail with the user, and follow the CLI confirmation flow before execution. <br>
Risk: The signup and OTP flows handle financial account setup and verification codes. <br>
Mitigation: Only request Ripio/tulebank credentials or OTP codes inside the intended CLI flow and do not expose them outside the command interaction. <br>


## Reference(s): <br>
- [ClawHub Tulebank release](https://clawhub.ai/aromeoes/tulebank) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with CLI command examples and human-readable summaries of JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the installed tulebank binary; transfer, swap, and on-ramp actions require user confirmation.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
