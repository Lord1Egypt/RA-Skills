## Description: <br>
Generate UUIDs in versions v1, v4, and v5 with options for count, namespace, name, and output format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darbling](https://clawhub.ai/user/darbling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate single or bulk UUID values for identifiers, test data, deterministic namespace IDs, or command-line workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: UUID v1 values can reveal generation timing and host-node metadata. <br>
Mitigation: Use UUID v4 for general or externally shared identifiers unless time-based UUIDs are specifically required. <br>
Risk: Generated identifiers may be treated as security secrets or proof of uniqueness beyond the UUID guarantees. <br>
Mitigation: Use UUIDs as identifiers only, and verify critical uniqueness or security requirements in the consuming system. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/darbling/uuid-gen-tools) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text UUID values, with one UUID per line for bulk output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports UUID v1, v4, and v5; format options include standard, uppercase, no-dashes, and URL-safe/no-dashes output.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
