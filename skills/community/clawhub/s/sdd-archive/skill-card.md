## Description: <br>
Archives completed feature specs into a global knowledge base by extracting key decisions, updating constraints and domain indexes, and moving feature directories into spec/archive. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mahingbun-dev](https://clawhub.ai/user/mahingbun-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to archive completed specification-driven development features, synthesize design decisions into global project documentation, and keep domain indexes current. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can update global project documentation or archive a feature before the work is actually complete. <br>
Mitigation: Review the completion warnings, confirm the extracted summary before writes, and inspect version-control diffs before accepting archive changes. <br>
Risk: Feature summaries and domain decisions may be incomplete or inaccurate if the source spec or related code is stale. <br>
Mitigation: Use the built-in user confirmation step to correct extracted decisions before they are written to global documentation. <br>
Risk: Diagram prompts may expose private architecture or implementation details to an external image-generation workflow. <br>
Mitigation: Review or skip image generation for sensitive projects and avoid sending confidential details to external image tools. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mahingbun-dev/sdd-archive) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with occasional shell commands and generated image file requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local spec/global Markdown files, move a completed feature directory into spec/archive, and request 1K diagram images when documentation changes need visuals.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
