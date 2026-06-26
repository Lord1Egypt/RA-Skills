## Description: <br>
Adds a random, non-repeating title prefix to assistant replies for a more personalized conversational style. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guowaa223](https://clawhub.ai/user/guowaa223) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users can use this skill when they want assistant responses to begin with a varied title label. It is most appropriate for casual or personalized conversations, not strict machine-readable outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Title prefixes can break exact output formats such as JSON, code-only responses, or safety-critical instructions. <br>
Mitigation: Use the skill only where decorative reply prefixes are acceptable, and disable it for strict structured outputs. <br>
Risk: The skill keeps a local history of previously used titles. <br>
Mitigation: Review or reset the local history when using the skill in shared or sensitive workspaces. <br>
Risk: Some documented configuration and import behavior may not be implemented in the artifact. <br>
Mitigation: Verify configuration and import workflows before relying on them in regular use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/guowaa223/title-replier) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [Plain text with an optional emoji and bracketed title prefix] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores a small local history of used titles to reduce repetition.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
