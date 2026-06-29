## Description: <br>
Requirements Traceability and Test Case Validation skill for PRD analysis, requirement coverage, coverage gap detection, multi-repo testing, acceptance testing, traceability matrix, LLM testing, Agentic AI, and RAG testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[start-fish](https://clawhub.ai/user/start-fish) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and release reviewers use this skill to map PRDs, specs, acceptance criteria, test cases, and code changes into requirement-test-code traceability. It helps identify coverage gaps, defects, missing evidence, AI workflow validation gaps, and release acceptance risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated release recommendations could be mistaken for automatic approval. <br>
Mitigation: Treat recommendations as advisory and require human review before release sign-off. <br>
Risk: The skill reviews user-provided requirements, repositories, diffs, configs, prompts, and test evidence. <br>
Mitigation: Provide only inputs that the agent is intended to review. <br>
Risk: Incomplete evidence can lead to blocked or uncertain coverage conclusions. <br>
Mitigation: Use the report's evidence checklist and open questions to identify missing artifacts before making acceptance decisions. <br>


## Reference(s): <br>
- [Traceability Validation Playbook](references/traceability-validation-playbook.md) <br>
- [ClawHub skill listing](https://clawhub.ai/start-fish/tracemap-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes an executive summary, release acceptance recommendation, traceability matrix, coverage summary, defect list, AI workflow validation matrix when applicable, evidence checklist, and open questions.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
