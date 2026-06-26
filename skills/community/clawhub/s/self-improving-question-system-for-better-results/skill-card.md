## Description: <br>
Diagnoses prompt quality and asks targeted clarification questions so an agent can produce more accurate, actionable, and rigorous answers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evafan7](https://clawhub.ai/user/evafan7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to improve underspecified requests before answer generation, especially when they need clearer output expectations, missing context, success criteria, or risk checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may interrupt immediate answer generation by asking clarification questions when a request is underspecified. <br>
Mitigation: Use it when answer quality depends on precise requirements, and allow the user to proceed when they do not want to add more context. <br>
Risk: Prompt-quality feedback can be overly forceful if applied to simple or already clear requests. <br>
Mitigation: Keep challenges specific to missing information and answer directly when the prompt passes the quality checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/evafan7/self-improving-question-system-for-better-results) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask targeted clarification questions before answering; stops when quality is sufficient, the user chooses to proceed, or the loop limit is reached.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
