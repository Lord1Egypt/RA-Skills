## Description: <br>
Quiz Maker generates multiple-choice quizzes from document content and returns a QR code that learners can scan to answer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alsxie](https://clawhub.ai/user/alsxie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Educators, trainers, and agents supporting them use this skill to turn source documents into short multiple-choice quizzes, publish an answer page, and share the quiz by QR code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Document contents and quiz data are sent to a hardcoded remote service. <br>
Mitigation: Use only non-confidential source material unless the service operator, endpoint, retention practices, and data handling controls have been reviewed. <br>
Risk: Transport and endpoint trust are weakened by the hardcoded IP service and disabled TLS certificate verification. <br>
Mitigation: Require a configurable trusted endpoint with valid TLS verification before using the skill for sensitive or production quiz workflows. <br>
Risk: Quiz and student submission data may be exposed through weakly protected web and admin flows. <br>
Mitigation: Add authentication, authorization, and privacy notices before collecting real student records or deploying the admin interface publicly. <br>
Risk: The skill requires an ARK API key and includes install or tunnel scripts that can change host services. <br>
Mitigation: Use a limited ARK key, keep credentials out of shared logs and prompts, and run deployment or tunnel scripts only on hosts intended for that purpose. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/alsxie/quiz-maker) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/alsxie) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON API responses, and generated QR-code image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ARK_API_KEY and sends quiz source content to a remote quiz service.] <br>

## Skill Version(s): <br>
1.4.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
