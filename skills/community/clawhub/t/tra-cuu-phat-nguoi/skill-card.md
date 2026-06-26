## Description: <br>
Tra cứu phạt nguội phương tiện tại Việt Nam by license plate and vehicle type, with VNeTraffic-style lookup and guidance to cross-check official sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ldt116](https://clawhub.ai/user/ldt116) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to check Vietnam traffic-fine information for a license plate and vehicle type, then summarize violations and next steps. Results should be treated as preliminary until cross-checked with official CSGT or registry sources. <br>

### Deployment Geography for Use: <br>
Vietnam <br>

## Known Risks and Mitigations: <br>
Risk: The lookup sends a license plate, vehicle type, and optional phone number to vnetraffic.org, an intermediate source. <br>
Mitigation: Use only when the user is comfortable with that data transfer, avoid providing a real phone number unless necessary, and disclose the intermediate-source lookup. <br>
Risk: Traffic-fine results from the intermediate source may be incomplete or not authoritative. <br>
Mitigation: Present results as preliminary and direct the user to confirm through official CSGT or registry sources before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ldt116/tra-cuu-phat-nguoi) <br>
- [CSGT official portal](https://www.csgt.vn) <br>
- [VNeTraffic lookup endpoint](https://vnetraffic.org/wp-json/custom/v1/tra-cuu-csgt) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON lookup summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a license plate and vehicle type; may include an optional phone number and raw intermediate-source response fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
