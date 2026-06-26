## Description: <br>
Compute SHA-256 cryptographic hash values for files and text. Use for secure data verification and integrity checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to calculate SHA-256 digests for local files when verifying downloads, checksums, and data integrity. It can guide an agent to run a minimal local hashing helper and return the resulting digest. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documentation shows a stdin usage example, but the included script reads a file path and falls back to a.txt when no argument is provided. <br>
Mitigation: Run the tool with an explicit file path and verify command mapping in the OpenClaw environment before relying on the result. <br>
Risk: Skill quality is marked low and quarantined for moderation review in the server evidence. <br>
Mitigation: Review the short implementation and documentation gaps before listing or deploying the skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dinghaibin/sha256-tool) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text hash digest and Markdown with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a SHA-256 hexadecimal digest for a local file path; the current script defaults to a.txt when no argument is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
