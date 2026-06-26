## Description: <br>
Generate daily or range-based lead summaries from read-only lead data for broker inventory counts, locality trends, and priority bucket breakdowns without ingestion, storage writes, or outbound communication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vishalgojha](https://clawhub.ai/user/vishalgojha) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External operators and review workflows use this skill to produce concise, date-range lead summaries from read-only lead records. It supports human review of broker inventory, buyer requirements, trends, localities, urgency, and priority counts before any downstream action suggestion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may summarize lead data outside the intended dataset or date range if deployed with overly broad read access. <br>
Mitigation: Limit runtime permissions to read-only, date-scoped access for the intended lead dataset. <br>
Risk: Downstream chained skills may turn summaries into action suggestions or external communications beyond this skill's boundaries. <br>
Mitigation: Review downstream chained skills separately before allowing them to suggest or perform actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/vishalgojha/summary-generator) <br>
- [summary-input.schema.json](references/summary-input.schema.json) <br>
- [summary-output.schema.json](references/summary-output.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Validated JSON summary object described by summary-output.schema.json] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only aggregate summary with zero-valued metrics when no leads exist and explicit failure reasons for query or validation errors.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
