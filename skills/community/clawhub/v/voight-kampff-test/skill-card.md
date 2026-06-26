## Description: <br>
Voight-Kampff Test is a Blade Runner-inspired empathy assessment that guides an agent through questions, scoring, and an informal human/replicant-style classification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aznikline](https://clawhub.ai/user/aznikline) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill for entertainment role-play and informal empathy-style questioning, producing an empathy index and classification. It should not be used for real identity, employment, security, legal, safety, or trust decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to collect sensitive emotional and behavioral observations and assign labels to a person or agent. <br>
Mitigation: Use it only as an explicit entertainment or role-play assessment, disclose the purpose before starting, allow questions to be skipped, and avoid storing or sharing responses without consent. <br>
Risk: The generated classification could be mistaken for a real identity, trust, employment, security, legal, or safety assessment. <br>
Mitigation: Present results as fictional and informal, and do not use them for consequential decisions or claims about a person's identity or trustworthiness. <br>
Risk: The referenced web version supports microphone-based interaction, which can introduce recording and site-trust concerns. <br>
Mitigation: Avoid the external microphone-enabled web version unless the user separately trusts the site and understands any recording or microphone behavior. <br>


## Reference(s): <br>
- [Voight-Kampff Test questions](references/questions.md) <br>
- [Voight-Kampff Test analysis guide](references/analysis.md) <br>
- [Command-line test runner](scripts/test_runner.py) <br>
- [Web version](https://aznikline.github.io/blade-runner-test/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown or plain text assessment report with interactive question prompts and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include an empathy score, classification, confidence, observations, and usage cautions.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
