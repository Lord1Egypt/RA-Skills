## Description: <br>
Searches text files or stdin for relevant lines, scores matches by keyword and phrase relevance, and returns matching excerpts with optional context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[indigas](https://clawhub.ai/user/indigas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to quickly locate relevant lines in large notes, logs, documents, or stdin before deciding whether to read the full file context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scanning private files can expose sensitive excerpts in terminal output or saved result files. <br>
Mitigation: Run the skill only on files the agent is permitted to inspect, review output before sharing it, and avoid using --output for sensitive results unless the destination is controlled. <br>
Risk: Line-level matches may omit surrounding context needed to interpret a result correctly. <br>
Mitigation: Use the returned line numbers and context window as a triage aid, then read the full source file section before relying on the excerpt. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/indigas/text-scan) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>
- [Artifact text-scan script](artifact/scripts/text-scan.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands] <br>
**Output Format:** [Plain text excerpts by default, brief line summaries when requested, or JSON arrays for programmatic use.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes line numbers, scores, matched terms, and configurable surrounding context; can write results to stdout or a user-specified output file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
