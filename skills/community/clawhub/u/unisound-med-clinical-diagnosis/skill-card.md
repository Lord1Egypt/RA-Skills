## Description:

Analyzes clinical case questions, supports differential diagnosis and primary-care diagnosis scenarios, and switches reasoning modes with --task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and clinical workflow integrators can pass de-identified medical questions to an internal medical LLM to obtain structured diagnostic reasoning or differential diagnosis support. Outputs are model-assisted information and should not be treated as formal clinical decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive clinical questions may be sent to the configured API endpoint and echoed in output.

Mitigation: Use only de-identified questions, avoid passing PHI on the command line, and keep outputs out of logs and shared artifacts.

Risk: Overriding --api-url can send bearer credentials and clinical content to an unintended endpoint.

Mitigation: Use only trusted HTTPS-protected endpoints with keys intended for that destination.

Risk: Medical model output can be incomplete, uncertain, or unsuitable for direct patient-care decisions.

Mitigation: Require qualified clinical review and follow institutional processes before using outputs in real workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-med-clinical-diagnosis)
- [Unisound-LLM publisher profile](https://clawhub.ai/user/unisound-llm)
- [Default model API endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON object by default; optional plain text answer with --text-only; optional NDJSON for batches.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write UTF-8 output files; dry-run mode returns parsed input without calling the model.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
