## Description:

Reviews insurance claim imaging or examination report text for a specified anatomical site and classifies the finding under the caller's injury categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Claims reviewers use this skill to submit de-identified imaging or examination report text and receive a structured auxiliary classification for chronic injury review. The result supports insurance review workflows and is not a forensic opinion or final claim decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive claim text or credentials could be sent to an unintended API endpoint.

Mitigation: Use only a trusted HTTPS API endpoint and protect and scope the appkey.

Risk: Claim materials may contain personal or medical identifiers.

Mitigation: De-identify claim materials before use.

Risk: Using output persistence can store the question, metadata, and model answer on disk.

Mitigation: Avoid --output unless disk storage of those contents is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-chronic-injury)
- [Publisher profile](https://clawhub.ai/user/unisound-llm)
- [Default medical model API endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON by default, or plain text when text-only output is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the skill name, status, selected model, input provenance fields, optional metadata, the original question, and the model answer.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
