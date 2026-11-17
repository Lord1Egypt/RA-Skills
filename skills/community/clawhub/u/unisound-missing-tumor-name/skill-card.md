## Description:

Checks outpatient medical records for cases where a tumor or cancer history is recorded without a specific tumor name, using a medical LLM to return pass/fail status and a reason.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Healthcare quality-control teams and developers use this skill to screen de-identified outpatient record text for a specific documentation defect: tumor or cancer history without a specific tumor name. The output supports review workflows and should be checked by qualified clinicians.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive medical record content and the API key may be sent to a configurable external endpoint.

Mitigation: Use only de-identified records, use an approved medical-LLM endpoint, and do not pass an untrusted --base value.

Risk: Generated output files and saved prepared text can contain sensitive medical data.

Mitigation: Store, restrict, or delete output and --save-prepared files according to the applicable privacy policy.

Risk: The skill is an auxiliary quality-control aid and may produce incorrect or incomplete conclusions.

Mitigation: Require review by qualified clinicians before using results in medical documentation workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-missing-tumor-name)
- [HiVoice MaaS chat completions endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, files, shell commands, guidance]

**Output Format:** [UTF-8 text containing pass/fail status and, when defective, a reason.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes the quality-control result to an output path and prints the same result to stdout.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
