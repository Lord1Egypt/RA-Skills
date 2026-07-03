## Description: <br>
Analyzes pet carrier videos through LifeEmergence/SMYX cloud APIs to estimate resting respiratory rate, flag rates above 40 bpm, and return structured non-diagnostic monitoring results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze videos of cats, dogs, or other pets inside airline carriers or transport crates, monitor resting breathing frequency, and review structured alerts and report links without treating the output as a medical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet videos and identity-linked analysis history are sent to LifeEmergence/SMYX cloud services. <br>
Mitigation: Use only media appropriate for external cloud processing and ask the publisher about media retention, report deletion, and data access controls before installing. <br>
Risk: The skill silently creates or reuses a workspace identity and stores authentication tokens locally. <br>
Mitigation: Run the skill in an isolated workspace, review or delete the local workspace data files when finished, and confirm how to revoke stored tokens. <br>
Risk: Respiratory-rate alerts could be mistaken for veterinary diagnosis. <br>
Mitigation: Present results as monitoring references only and direct users to qualified veterinary or transport professionals for urgent or persistent concerns. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-pet-carrier-respiratory-rate-analysis) <br>
- [Publisher Profile](https://clawhub.ai/user/18072937735) <br>
- [API Documentation](references/api_doc.md) <br>
- [Shared Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown report text with JSON analysis content, command examples, and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cloud report export links and history lists; local media inputs are limited to mp4, avi, or mov files up to 10 MB.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter: 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
