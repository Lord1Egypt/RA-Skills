## Description: <br>
Generate and parse UUIDs (v1, v4, v5), including batch generation, validation, and format conversion with the Python standard library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate UUIDs, validate UUID strings, parse UUID components, and convert UUID formatting for application identifiers and scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: UUID v1 values can reveal timestamp and machine-related metadata. <br>
Mitigation: Prefer UUID v4 for public, shared, or privacy-sensitive identifiers; use UUID v1 only when time-based identifiers are specifically needed. <br>
Risk: The reviewed artifacts do not require credentials, so providing secrets would create unnecessary exposure. <br>
Mitigation: Do not provide API keys, tokens, passwords, or other credentials when using this skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/uuid-generator-tool) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates UUID strings and validation or parsing summaries; no external services are required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
