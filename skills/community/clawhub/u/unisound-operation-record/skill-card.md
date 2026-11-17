## Description:

Generates standardized surgical operation records from preoperative, intraoperative, and postoperative clinical materials using an internal medical large language model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and clinical documentation teams use this skill to turn de-identified surgical source materials into standardized operation-record drafts for medical record workflows. Generated records require clinician review before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive clinical text may be exposed if records are not de-identified before model calls.

Mitigation: Use only de-identified records and review the skill before installing it in healthcare or PHI-adjacent workflows.

Risk: The remote model endpoint is configurable and could send clinical content to an unapproved service.

Mitigation: Keep --base pinned to an approved internal HTTPS endpoint.

Risk: The appkey credential can be exposed through command history or process handling.

Mitigation: Protect the appkey outside command history wherever possible.

Risk: Generated operation records may be incomplete or clinically inaccurate.

Mitigation: Require clinician review of generated records before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-operation-record)
- [Internal medical LLM API endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration]

**Output Format:** [UTF-8 surgical operation record text, with optional JSON or text file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires de-identified clinical input and an appkey for the configured medical LLM endpoint.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact _meta.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
