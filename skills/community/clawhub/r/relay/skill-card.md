## Description: <br>
Relay provides a CLI-style local entry store for adding, listing, searching, removing, exporting, and configuring relay-labeled records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can ask an agent to run or explain Relay commands for maintaining a simple local record store, including adding, listing, searching, removing, exporting records, and checking basic status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is advertised as a relay logic and wiring helper, but the security summary says it behaves as a local persistent note and configuration manager. <br>
Mitigation: Use it only for simple local records, and do not rely on it for relay logic validation, wiring diagrams, or operational electrical guidance. <br>
Risk: User-entered data can be stored in plaintext under ~/.relay or RELAY_DIR and exported to local files. <br>
Mitigation: Avoid entering secrets, plant details, or sensitive operational notes; review add, remove, export, and config commands before running them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckchzh/relay) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and local command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may create, delete, search, and export plaintext local records under ~/.relay or RELAY_DIR.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
