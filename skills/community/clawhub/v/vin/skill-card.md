## Description: <br>
Uses JisuAPI to query vehicle details from a 17-character VIN and retrieve oil or gearbox information by vehicle model ID. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to answer VIN lookup requests, summarize vehicle attributes, and request related oil or gearbox details from JisuAPI when the user provides a VIN or carid. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: VINs and vehicle model IDs are sent to JisuAPI, which may expose personal, fleet, or otherwise sensitive vehicle data to a third-party API provider. <br>
Mitigation: Use a dedicated JISU_API_KEY with quota limits, query only VINs or carids the user is authorized to share, and avoid using the skill for sensitive fleet or personal vehicle data without permission. <br>
Risk: The Python script depends on the local requests package and executes outbound HTTPS requests. <br>
Mitigation: Run the skill in a trusted Python environment and install dependencies from trusted package sources before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/vin) <br>
- [JisuAPI VIN documentation](https://www.jisuapi.com/api/vin/) <br>
- [JisuAPI provider site](https://www.jisuapi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON from a Python CLI, with Markdown usage guidance in the skill instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, requests, and JISU_API_KEY; sends VIN or carid inputs to JisuAPI.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
