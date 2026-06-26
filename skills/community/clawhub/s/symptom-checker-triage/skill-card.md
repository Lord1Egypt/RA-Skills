## Description: <br>
Suggest triage levels (Emergency, Urgent, Outpatient) based on red flag symptoms using a rule-based engine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to triage natural-language symptom descriptions into Emergency, Urgent, or Outpatient levels and produce structured rationale, red flags, recommendations, and safety disclaimers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical triage output may be wrong, incomplete, or overconfident because it is a lightweight rule-based aid. <br>
Mitigation: Preserve the warning on every response, avoid presenting results as diagnosis or treatment, and route urgent or unclear symptoms to professional medical care. <br>
Risk: Emergency-service instructions may be region-specific if the response tells users to call 911. <br>
Mitigation: Tell users to contact their local emergency number unless the deployment context confirms 911 is appropriate. <br>
Risk: The skill can be misused for diagnosis, prescriptions, lab interpretation, or general medical advice outside its stated scope. <br>
Mitigation: Limit use to symptom-triage descriptions and refuse out-of-scope medical requests using the documented scope message. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/symptom-checker-triage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown triage report or JSON object with triage level, confidence, red flags, rationale, recommendation, department, and warning.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Rule-based local output; every result should preserve the medical disclaimer and direct urgent or unclear cases to professional care.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
