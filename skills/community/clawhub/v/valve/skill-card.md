## Description: <br>
Advertised as a valve sizing and selection tool, this skill provides shell commands for a local entry log. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators can use this skill to run a local CLI that records, lists, searches, removes, and exports entries. It should not be used for valve sizing or safety-critical engineering decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The advertised valve sizing purpose does not match the artifact behavior. <br>
Mitigation: Review the shell script before use and do not rely on it for valve sizing, selection, or safety-critical engineering work. <br>
Risk: The skill stores, deletes, and exports local entries. <br>
Mitigation: Avoid storing secrets or sensitive operational data, set VALVE_DIR to an appropriate local directory, and review deletion or export commands before running them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xueyetianya/valve) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, text, configuration, files] <br>
**Output Format:** [Plain text stdout with local JSONL storage and optional JSON or CSV export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes to ~/.valve by default unless VALVE_DIR is set; export commands write valve-export files in the current directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
