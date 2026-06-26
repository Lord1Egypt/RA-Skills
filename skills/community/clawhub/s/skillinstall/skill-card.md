## Description: <br>
Install OpenClaw skills from clawhub.ai ZIP files with automatic detection, validation, and Gateway updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[otho2966-ai](https://clawhub.ai/user/otho2966-ai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install downloaded ClawHub skill ZIPs into a local OpenClaw installation, validate basic skill structure, list installed skills, and restart the Gateway when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ZIP installation has a path traversal risk when handling untrusted archives. <br>
Mitigation: Install only trusted or reviewed ZIP files, inspect archive paths before installation, and avoid arbitrary ZIP files until path traversal is fixed. <br>
Risk: The installer modifies the local OpenClaw skills directory and can overwrite existing skills. <br>
Mitigation: Run with the least required privileges, confirm the target install path, and review existing skills before allowing overwrite. <br>
Risk: The skill's validation checks basic structure and should not be treated as a full safety review. <br>
Mitigation: Review and scan each skill package before deployment, especially packages from unknown publishers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/otho2966-ai/skillinstall) <br>
- [Skill README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and write access to the local OpenClaw skills directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, changelog dated 2025-02-26) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
