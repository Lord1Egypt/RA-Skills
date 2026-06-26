## Description: <br>
Final quality validation gate for artifacts before human review, covering factual accuracy, tone, completeness, structure, operational soundness, and sensitive data handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[corbin-breton](https://clawhub.ai/user/corbin-breton) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and release reviewers use this skill to validate documents, code artifacts, skills, PRDs, and publication drafts before human review or release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may push the agent beyond read-only review by asking it to fix failed artifacts or write QA reports. <br>
Mitigation: Ask the agent to produce findings and proposed edits first, and review any diff before allowing changes or saved reports. <br>
Risk: QA reports may include sensitive content copied or summarized from reviewed artifacts. <br>
Mitigation: Review report contents before sharing or publishing, and avoid saving confidential details unless they are required for the review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/corbin-breton/qa-gate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown validation report with PASS, PASS WITH FIXES, or FAIL verdict and severity-tagged findings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask the agent to write a QA report and to fix or propose fixes for critical and major findings.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
