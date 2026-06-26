## Description: <br>
通过 17 位 VIN 车架号与待译码的配件别名列表，精准解出这些配件的标准配件编码 OE 与标准配件名称等信息。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[polaris2013](https://clawhub.ai/user/polaris2013) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Parts, repair, and automotive workflow users can provide a 17-character VIN and a list of part aliases to retrieve standard OE part codes, standard part names, and related pricing fields through the disclosed provider API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: VINs, requested part names, and requests tied to JZ_API_KEY are sent to the disclosed external API. <br>
Mitigation: Use the skill only when that data sharing is approved, and prefer a dedicated provider API key. <br>
Risk: Vehicle data may be confidential under an organization's internal policies. <br>
Mitigation: Avoid submitting confidential vehicle data unless the organization has approved use of the provider service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/polaris2013/vinoe) <br>
- [VIN-PARTSNAME API endpoint](https://erp.qipeidao.com/jzOpenClaw/getVinOe) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [JSON from the command-line helper, with text guidance for setup and interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JZ_API_KEY; sends VIN and part-name queries to the disclosed external API.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
