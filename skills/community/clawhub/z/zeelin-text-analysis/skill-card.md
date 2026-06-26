## Description: <br>
Analyzes uploaded text files by extracting entities, generating relationship information, and producing character or document profiles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liyayong000-sketch](https://clawhub.ai/user/liyayong000-sketch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to send local text documents to the Zeelin analysis service and receive structured analysis results as Markdown. It is intended for document, novel, or text-processing workflows that need entity extraction, relationship summaries, and profile organization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads selected documents and an App-Key to an unencrypted raw-IP service with unclear privacy and retention controls. <br>
Mitigation: Install only if you trust the Zeelin service, avoid confidential or regulated files, use a restricted or easily rotated key, and verify whether an HTTPS endpoint and privacy policy are available. <br>
Risk: Generated Markdown analysis results may remain on disk. <br>
Mitigation: Review generated files before sharing them and delete outputs that contain sensitive or regulated content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liyayong000-sketch/zeelin-text-analysis) <br>
- [Zeelin service website](https://skills.zeelin.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown analysis report with API request examples and JSON configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce an .md result file after polling an external analysis task.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
