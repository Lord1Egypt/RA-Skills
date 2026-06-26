## Description: <br>
Unit converts common measurement categories and more than 150 currencies, using offline conversion factors for physical units and live exchange rates when network access is available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlang-cn](https://clawhub.ai/user/openlang-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Unit to answer unit-conversion requests across length, weight, area, volume, temperature, time, speed, data storage, energy, power, pressure, and currency. It can return offline conversions directly or use live exchange-rate data for currency conversions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Currency conversion may make outbound network requests to exchangerate.host. <br>
Mitigation: Use offline unit conversions only in environments that prohibit outbound network access. <br>
Risk: Currency conversion stores a small local exchange-rate cache. <br>
Mitigation: Review local cache handling before use in environments with strict file-write or data-retention policies. <br>
Risk: Live currency rates fluctuate and may not match transaction rates. <br>
Mitigation: Treat currency results as estimates and confirm financial transactions against an authoritative provider. <br>


## Reference(s): <br>
- [ClawHub Unit skill page](https://clawhub.ai/openlang-cn/unit) <br>
- [exchangerate.host](https://exchangerate.host) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text conversion results and Markdown guidance with bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Currency conversion may contact exchangerate.host and cache exchange rates locally for one hour.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
