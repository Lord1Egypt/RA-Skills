## Description: <br>
Control Word app sessions, documents, selections, comments, export, and review state with osascript workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users on macOS use this skill to control live Microsoft Word sessions when the current document, selection, comments, tracked changes, review state, or Word-native export behavior matters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live Word automation can edit, export, overwrite, accept or reject changes, or close documents in the wrong scope. <br>
Mitigation: Confirm the exact document, action scope, reversibility, and output path before risky actions; read state before mutation and verify the final state afterward. <br>
Risk: Selection-driven edits or document-wide review actions can affect the wrong paragraph, story range, comments, or tracked changes. <br>
Mitigation: Prefer object-anchored actions when possible, clarify ambiguous selections, and require explicit confirmation for bulk accept, reject, delete, overwrite, or close-without-save actions. <br>
Risk: Local Word memory files may persist document paths, environment notes, or workflow details. <br>
Mitigation: Keep memory limited to non-sensitive environment facts and reusable workflow notes; do not store document contents, secrets, or personal information. <br>


## Reference(s): <br>
- [ClawHub Word Skill](https://clawhub.ai/ivangdavila/word) <br>
- [Word Skill Homepage](https://clawic.com/skills/word) <br>
- [Execution Matrix](artifact/execution-matrix.md) <br>
- [Live Control Patterns](artifact/live-control-patterns.md) <br>
- [Safety Checklist](artifact/safety-checklist.md) <br>
- [Setup](artifact/setup.md) <br>
- [Troubleshooting](artifact/troubleshooting.md) <br>
- [Memory Template](artifact/memory-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with AppleScript and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local macOS Word automation guidance and commands; the skill itself does not call cloud document APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
