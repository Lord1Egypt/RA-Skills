## Description: <br>
Generate, parse, validate, and convert UUIDs (v1/v3/v4/v5), ULIDs, and NanoIDs for identifier creation, inspection, validation, format conversion, and bulk generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnywang2001](https://clawhub.ai/user/Johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to ask an agent for local commands or code-oriented guidance that generate, parse, validate, and convert common identifier formats. It is useful for application development, debugging identifier data, and producing bulk UUID, ULID, NanoID, or nil UUID values. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: UUIDv1 identifiers can expose creation time and device-like node metadata. <br>
Mitigation: Prefer UUIDv4, ULID, or NanoID for privacy-sensitive identifiers, and avoid UUIDv1 when timestamp or node metadata should not be shared. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Johnnywang2001/uuid-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated identifier strings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local Python 3.9+ command examples; no external dependencies are required by the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
