## Description: <br>
Provides health consultation, health-check interpretation, and triage department recommendations through task-selected medical model prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and healthcare workflow integrators use this skill to route user-provided health questions to a configured medical LLM for general health Q&A, health-check interpretation, or department triage recommendations. Outputs are assistive information and should not be treated as formal clinical decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Health questions are sent to the configured medical model endpoint. <br>
Mitigation: Avoid identifiable patient information unless the workflow has been approved by the organization; use --dry-run to inspect parsed input before making a network call. <br>
Risk: Model answers may be mistaken for clinical decisions. <br>
Mitigation: Present outputs as assistive information and require appropriate clinical or institutional review for real patient care. <br>
Risk: The API key is provided on the command line or by the calling workflow. <br>
Mitigation: Keep the key in an approved secret-handling path and avoid logging command invocations that include credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-med-health-consult) <br>
- [Publisher profile](https://clawhub.ai/user/unisound-llm) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [JSON by default, with optional plain text answer output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write full results to a file; batch JSONL input emits NDJSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
