## Description:

Helps select the most likely CHS-DRG group from supplied discharge-case text and candidate DRG options using a configured medical model endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Clinicians, medical coding reviewers, and evaluation engineers use this skill to run DRG candidate selection against case prompts or datasets and compare model-selected groupings with expected results. The output is decision support only and is not a formal insurance settlement or hospital grouping conclusion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive medical case text or the API key could be exposed through the configured model endpoint or saved output files.

Mitigation: Use only the documented default or another approved HTTPS endpoint, de-identify real patient data, protect the appkey, and store output files only in locations approved for medical data.

Risk: The selected DRG is model-generated decision support and may be incorrect.

Mitigation: Review results through the applicable clinical coding and hospital governance workflow before using them for reimbursement, settlement, or operational decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-drg-grouping)

## Skill Output:

**Output Type(s):** [text, JSON, files]

**Output Format:** [JSON stdout by default, with optional plain text answer output or JSON/NDJSON output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include answer, question, meta, record_index, model, input_mode, and input_path fields; batch JSONL input emits NDJSON.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
