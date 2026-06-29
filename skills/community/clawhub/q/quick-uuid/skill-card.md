## Description: <br>
Generate UUIDs (v4) and short random IDs from the command line. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate UUID v4 values or short URL-safe random IDs for files, records, test fixtures, logs, and correlation IDs without adding dependencies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Short random IDs are convenient but not guaranteed unique at large scale. <br>
Mitigation: Use UUID v4 for stronger practical uniqueness, or check generated short IDs against the target datastore before accepting them. <br>
Risk: Identifiers used for security-adjacent purposes need cryptographically strong randomness. <br>
Mitigation: Use the documented Python secrets-based command for short IDs and avoid non-cryptographic random generators. <br>


## Reference(s): <br>
- [Quick UUID on ClawHub](https://clawhub.ai/terrycarter1985/quick-uuid) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local command-line one-liners for UUID v4 and short random ID generation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
