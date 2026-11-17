## Description:

Checks outpatient medical record text for inconsistency between the chief complaint and history of present illness, then returns a no-defect result or a defect result with the reason.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Clinicians, medical quality reviewers, and healthcare developers use this skill to check whether an outpatient record's chief complaint is consistent with the history of present illness. The result is advisory and should be reviewed by a qualified clinician.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive clinical text may be sent to a remote LLM endpoint.

Mitigation: Use only de-identified records in environments approved for medical data, and keep the base URL fixed to a trusted HTTPS endpoint.

Risk: Plaintext results may be written to local output paths.

Mitigation: Direct outputs to controlled private storage and apply retention cleanup after review.

Risk: The model result may be incomplete or incorrect for clinical quality decisions.

Mitigation: Treat outputs as advisory and require review by a qualified clinician.

Risk: The appkey grants access to the remote model service.

Mitigation: Use a least-privilege appkey and do not store credentials in the repository.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-chief-complaint-hpi-inconsistent)
- [HiVoice MaaS chat completions endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration]

**Output Format:** [UTF-8 plain text containing a no-defect result or a defect result with a reason.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a HiVoice MaaS appkey and de-identified outpatient medical record input; writes plaintext output to a controlled local path.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
