## Description: <br>
Extracts health-exam findings that need recheck, grades urgency, and produces structured follow-up items plus patient-facing reminder text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Health exam centers and health management teams use this skill to convert exam report text into a recheck checklist with urgency windows, departments, venues, preparation steps, and a concise reminder for the examinee. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Health exam report text may be sent to a configured remote model endpoint and can contain sensitive medical or identifying information. <br>
Mitigation: Use only with organizational approval for the endpoint, remove names, IDs, phone numbers, and other identifiers before running, and verify endpoint retention terms. <br>
Risk: The release claims de-identification, but the security evidence says the code does not perform that de-identification itself. <br>
Mitigation: Perform de-identification before invoking the skill and do not rely on the skill as the privacy control. <br>
Risk: Saved output files may contain sensitive health follow-up details. <br>
Mitigation: Choose approved storage locations for --output files, apply access controls, and delete outputs according to organizational retention policy. <br>
Risk: The default timeout can wait indefinitely for the remote model call. <br>
Mitigation: Set a finite --timeout value that matches operational requirements. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/unisound-llm/unisound-recheck-reminder) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files] <br>
**Output Format:** [JSON followed by a plain-language recheck reminder; optionally written to a UTF-8 output file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a configured remote medical model endpoint and can print to stdout or save to an --output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
