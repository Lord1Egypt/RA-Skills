## Description: <br>
PDF processing and manipulation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other agent users can use this skill to scope PDF processing and manipulation tasks, then have the agent choose appropriate file, shell, or web tools for the requested operation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF actions can target the wrong document or perform unintended shell commands if the user request is vague. <br>
Mitigation: Give the agent explicit file paths and requested operations, and require confirmation before shell commands or file writes. <br>
Risk: Sensitive documents could be exposed if an external Nano PDF service or upload path is used without review. <br>
Mitigation: Verify any Nano PDF service before use and avoid providing sensitive documents unless the service and destination are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/terry-nano-pdf) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with optional inline shell commands and file-operation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; no executable code is bundled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
