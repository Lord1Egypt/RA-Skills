## Description: <br>
Use Chanjing customised person APIs to create, inspect, list, poll, and delete custom digital humans from uploaded source videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zuoyuting214](https://clawhub.ai/user/zuoyuting214) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to work with Chanjing custom digital-human assets: uploading source videos, creating custom persons, checking status and details, listing existing persons, and deleting assets when no longer needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses local Chanjing app_id, secret_key, and cached access tokens. <br>
Mitigation: Keep CHANJING_CONFIG_DIR pointed at a private trusted directory, protect credentials from chat and logs, and rotate credentials if they may have been exposed. <br>
Risk: The skill can upload source videos to Chanjing services. <br>
Mitigation: Use it only for videos the user intends to upload and is authorized to process. <br>
Risk: The skill can delete custom digital-human assets. <br>
Mitigation: Confirm the exact person ID and intended target before running delete actions. <br>
Risk: CLI examples reference operational scripts that are not present in the provided artifact. <br>
Mitigation: Verify the operational scripts exist in the installed skill before relying on the documented CLI flows. <br>


## Reference(s): <br>
- [Chanjing Open API](https://open-api.chanjing.cc) <br>
- [Reference](reference.md) <br>
- [Examples](examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON or plain-text script outputs such as file IDs, person IDs, preview URLs, and API details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Chanjing credentials and may return remote asset URLs; preview resources are not downloaded unless explicitly requested.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
