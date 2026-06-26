## Description: <br>
Build REST API specifications for Sling data extraction, including authentication, pagination, response processing, rate limiting, endpoint chaining, and incremental sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flarco](https://clawhub.ai/user/flarco) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and data engineers use this skill to create and validate Sling YAML specs for extracting data from REST APIs. It is most useful when configuring authentication, endpoint requests, pagination, response transformations, endpoint queues, and incremental sync behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or adapted API specs can request broad credentials or scopes. <br>
Mitigation: Review API scopes and credentials before running any generated Sling spec. <br>
Risk: Setup or teardown sequences can use POST or DELETE operations that create, modify, or remove remote resources. <br>
Mitigation: Inspect setup and teardown steps before execution, especially non-GET requests. <br>
Risk: Queue or sync values can temporarily hold sensitive data if specs store more than identifiers or cursors. <br>
Mitigation: Keep queue and sync values limited to IDs, cursors, timestamps, or other low-sensitivity values. <br>


## Reference(s): <br>
- [Sling API Specs Documentation](https://docs.slingdata.io/concepts/api-specs.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/flarco/sling-api-specs) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown with YAML and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance for authoring Sling REST API specification files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
