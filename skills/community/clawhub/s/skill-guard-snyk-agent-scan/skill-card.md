## Description: <br>
Scans ClawHub skills with Snyk Agent Scan before installation to detect prompt injections, malware payloads, hardcoded secrets, and other threats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[firefrog-pepe](https://clawhub.ai/user/firefrog-pepe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to scan a ClawHub skill in a staging area before installing it into an OpenClaw workspace. It helps identify security issues, scanner setup failures, and cases that need manual review before a skill is trusted by an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The wrapper can modify the local OpenClaw skills directory after staging and scanning a skill. <br>
Mitigation: Use the default scan path, inspect staged files and scan reports when needed, and use --force only when intentionally replacing an installed skill. <br>
Risk: A missing or invalid SNYK_TOKEN prevents the Snyk Agent Scan from completing, and --skip-scan bypasses the main safety gate. <br>
Mitigation: Configure SNYK_TOKEN before use and reserve --skip-scan for deliberate manual-review cases where the installation risk is accepted. <br>
Risk: The workflow depends on external command-line tooling and recommends a curl-to-shell uv installation path in the skill documentation. <br>
Mitigation: Install dependencies through verified package-manager or vendor-approved channels and review the scanner command path before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/firefrog-pepe/skill-guard-snyk-agent-scan) <br>
- [Publisher profile](https://clawhub.ai/user/firefrog-pepe) <br>
- [uv installer referenced by the skill](https://astral.sh/uv/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash command examples and shell output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May stage skills under /tmp, write scan reports, and install into the configured OpenClaw skills directory when invoked.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
