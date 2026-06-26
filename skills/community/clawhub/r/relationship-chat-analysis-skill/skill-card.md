## Description: <br>
Analyzes explicitly supplied relationship chat records by cleaning noisy exports, segmenting episodes, and producing evidence-grounded communication, conflict, repair, safety, and blind-spot analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yujun-bo2](https://clawhub.ai/user/yujun-bo2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to analyze long romantic or relationship chat histories that the user intentionally provides, with emphasis on recurring communication patterns, conflict cycles, repair attempts, boundaries, effort balance, and unsupported conclusions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Relationship chats can contain intimate content, identifiers, third-party details, abuse disclosures, or other sensitive information. <br>
Mitigation: Process only chats the user explicitly provides or identifies, minimize retained content, redact unnecessary identifiers, and avoid storing raw full chat logs. <br>
Risk: Generated reports or manifests written to local storage may persist in backups, sync tools, search indexes, or later processes. <br>
Mitigation: Tell the user the planned output paths and write files only after consent or an explicit file-output request. <br>
Risk: Relationship analysis can overstate motives, diagnoses, or conclusions not supported by the messages. <br>
Mitigation: Ground major claims in dated examples or short quotes, separate observation from interpretation, state uncertainty, and avoid clinical or legal conclusions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yujun-bo2/relationship-chat-analysis-skill) <br>
- [README](README.md) <br>
- [Detailed orchestration guide](references/instructions.md) <br>
- [Chat cleaning and normalization prompt](references/cleaning-prompt.md) <br>
- [Episode-level extraction prompt](references/extraction-prompt.md) <br>
- [Cross-episode synthesis prompt](references/synthesis-prompt.md) <br>
- [Blind spot and safety review prompt](references/blindspot-prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown relationship analysis report with optional redacted JSON corpus manifest] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should use short evidence quotes, redact unnecessary identifiers, avoid raw full chat logs, and separate observations from interpretations and uncertainty.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
