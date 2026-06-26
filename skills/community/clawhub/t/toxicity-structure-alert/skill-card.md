## Description: <br>
Analyze data with `toxicity-structure-alert` using a reproducible workflow, explicit validation, and structured outputs for review-ready interpretation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and chemoinformatics reviewers use this skill to screen chemical structure inputs such as SMILES for known toxic structural alerts, risk levels, and review-ready recommendations. Its results are screening signals for expert review, not a substitute for comprehensive toxicological assessment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screening output may be mistaken for definitive toxicology assessment. <br>
Mitigation: Treat results as screening signals and require expert toxicology validation before scientific, clinical, or product decisions. <br>
Risk: Dependency hygiene issues or unpinned chemistry dependencies can create deployment drift. <br>
Mitigation: Install in an isolated Python environment, prefer a trusted RDKit source, and pin or remove dependencies before production use. <br>
Risk: Non-chemical inputs can produce irrelevant or misleading results. <br>
Mitigation: Use only chemical structure inputs such as SMILES or SMARTS and validate the input format before running the skill. <br>


## Reference(s): <br>
- [Runtime Checklist](references/runtime_checklist.md) <br>
- [ClawHub release page](https://clawhub.ai/aipoch-ai/toxicity-structure-alert) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Text or JSON, with concise Markdown guidance and validation commands when appropriate] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include risk level, risk score, matched alerts, recommendations, and assumptions or limits that affect interpretation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
