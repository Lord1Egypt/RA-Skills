## Description: <br>
Scan ClawHub skills for security vulnerabilities BEFORE installing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenswj](https://clawhub.ai/user/kenswj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to stage ClawHub skill installs, scan the staged content with mcp-scan, and install only when no security issues are detected. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The shell wrapper can modify the OpenClaw skills directory and replace existing skills when forced. <br>
Mitigation: Use known-good ClawHub slugs, avoid --force unless replacement is intended, and review the staged skill before installation. <br>
Risk: The --skip-scan option bypasses the security gate the skill is intended to provide. <br>
Mitigation: Do not use --skip-scan for normal installs; allow mcp-scan to run before moving staged content into the skills directory. <br>
Risk: The workflow depends on external CLI tooling and latest scanner resolution. <br>
Mitigation: Prefer pinned or verified installations for uv and mcp-scan before using the wrapper in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kenswj/skill-guard-1-0-2) <br>
- [mcp-scan](https://github.com/invariantlabs-ai/mcp-scan) <br>
- [uv Installer](https://astral.sh/uv/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal output and Markdown with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit codes distinguish clean installs, dependency or network errors, and quarantined threat findings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact _meta.json lists 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
