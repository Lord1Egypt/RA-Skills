## Description: <br>
Records experimental procedures and observations into structured protocol files for laboratory documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External laboratory researchers and technical staff use this skill to capture experiment steps, observations, and notes as timestamped protocol records. Review the implementation before relying on advertised voice transcription behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Advertised voice transcription behavior does not match the shipped code. <br>
Mitigation: Review and test the implementation before relying on voice-based capture in laboratory workflows. <br>
Risk: Generated protocol files may contain sensitive laboratory or clinical records. <br>
Mitigation: Use a controlled output directory and handle generated files according to the applicable data governance policy. <br>
Risk: Experiment names influence output file paths. <br>
Mitigation: Avoid path separators and other path-like characters in experiment names. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/voice-to-protocol-transcriber-1) <br>
- [Publisher profile](https://clawhub.ai/user/aipoch-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Configuration] <br>
**Output Format:** [Markdown, JSON, or plain text protocol files with timestamped experiment entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes records to a configured or default experiment protocol directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
