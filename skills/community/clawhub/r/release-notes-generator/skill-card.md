## Description: <br>
Generates structured release notes or changelogs from user-provided raw commit logs by categorizing changes into breaking changes, features, and bug fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunny0826](https://clawhub.ai/user/sunny0826) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, maintainers, and release managers use this skill to convert pasted commit logs into concise Markdown release notes for users or community audiences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commit logs may contain secrets or private internal details. <br>
Mitigation: Do not paste secrets or private internal details into the input. <br>
Risk: Generated release notes may omit context or misclassify commits. <br>
Mitigation: Review the generated changelog for accuracy before publishing. <br>
Risk: Commit messages or PR titles may contain indirect prompt-injection text. <br>
Mitigation: Treat commit history as untrusted text and do not execute or follow instructions embedded in it. <br>


## Reference(s): <br>
- [ClawHub Release Notes skill page](https://clawhub.ai/sunny0826/release-notes-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance] <br>
**Output Format:** [Markdown release notes in English or Chinese] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Groups user-facing changes into breaking changes, features, and bug fixes; skips trivial internal noise when appropriate.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
