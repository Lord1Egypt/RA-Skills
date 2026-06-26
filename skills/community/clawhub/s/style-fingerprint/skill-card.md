## Description: <br>
Analyzes Chinese writing style from text or files, saves local JSON fingerprints, and exports compact style guides for writing agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noah-1106](https://clawhub.ai/user/noah-1106) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and writing agents use this skill to analyze Chinese prose, persist reusable style fingerprints, and export compact style guidance for later drafting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence rates the skill suspicious because it can read, write, and delete local files more broadly than the documentation makes obvious. <br>
Mitigation: Review before installation and run it only in workspaces where local file reads, writes, and deletes are acceptable. <br>
Risk: Fingerprint names influence local JSON file paths. <br>
Mitigation: Use simple fingerprint names without slashes, absolute paths, or '..'. <br>
Risk: Analyzed text may leave a retained local excerpt in the saved fingerprint. <br>
Mitigation: Avoid confidential drafts unless local retention is acceptable, and delete fingerprints that should not persist. <br>
Risk: Export output paths can create or overwrite files. <br>
Mitigation: Export only to paths the user explicitly intends to create or replace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/noah-1106/style-fingerprint) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON files, Shell commands, Guidance] <br>
**Output Format:** [Command-line text output, local JSON fingerprint files, and exported Markdown or text style guides] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and writes fingerprints under ./fingerprints/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
