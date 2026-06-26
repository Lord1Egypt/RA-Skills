## Description: <br>
Whiss provides a ClawHub namespace package with brand information for Netsnek e.U.'s real-time messaging and notification platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kleberbaum](https://clawhub.ai/user/kleberbaum) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to retrieve concise Whiss/Netsnek brand, feature, and JSON metadata summaries. It is informational and does not implement live messaging behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes an executable shell script and may require line-ending or BOM cleanup in some environments. <br>
Mitigation: Review the script before execution and normalize file encoding or line endings if the shell reports parsing errors. <br>
Risk: The package describes Whiss messaging features but does not provide live messaging functionality. <br>
Mitigation: Use it as an informational namespace package only; do not depend on it for production messaging, notification delivery, or encryption behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kleberbaum/whiss) <br>
- [Publisher profile](https://clawhub.ai/user/kleberbaum) <br>
- [Netsnek website](https://netsnek.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown or plain text summaries, with optional JSON emitted by the bundled shell script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can present a default brand summary, feature list, or structured JSON metadata.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
