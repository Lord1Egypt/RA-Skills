## Description: <br>
Creates and verifies OpenTimestamps proofs that anchor local file hashes to the Bitcoin blockchain. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axhoff](https://clawhub.ai/user/axhoff) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to create timestamp proofs for important workspace files, verify existing .ots proof files, and archive older proofs when file contents change. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The OpenTimestamps client runs from the local Python environment and is invoked by the skill's shell scripts. <br>
Mitigation: Install the OpenTimestamps client only from a trusted Python environment and review the resolved OTS_BIN before use. <br>
Risk: Proof files can reveal file existence, timing, and grouping even though the scripts do not upload file contents. <br>
Mitigation: Treat .ots files and archive directories as metadata-bearing artifacts, and timestamp files separately with delays when linkability matters. <br>
Risk: A valid timestamp proves that exact bytes existed by a time, but does not prove the content is true or safe. <br>
Mitigation: Use timestamp verification as integrity evidence only, and independently review the underlying file content before trusting it. <br>


## Reference(s): <br>
- [Timestamp ClawHub listing](https://clawhub.ai/axhoff/timestamp) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local .ots proof files and verification summaries through shell scripts that call the OpenTimestamps client.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
