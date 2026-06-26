## Description: <br>
Segway device integration skill for interacting with, diagnosing, configuring, and troubleshooting Segway balance vehicles and electric vehicles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aNinebot](https://clawhub.ai/user/aNinebot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to get agent guidance for connecting to Segway devices, reading battery, mileage, and firmware status, configuring vehicle settings, diagnosing faults, and exporting ride statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Factory reset, speed-limit changes, and other vehicle-setting changes can affect vehicle operation. <br>
Mitigation: Require explicit user confirmation, keep the vehicle stopped, and back up current settings before applying high-impact changes. <br>
Risk: Exported ride or diagnostic data may include device or usage information. <br>
Mitigation: Review exported data before sharing it and remove sensitive device or usage details when they are not needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include diagnostic suggestions, vehicle-setting guidance, and ride-data export guidance for user review.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
