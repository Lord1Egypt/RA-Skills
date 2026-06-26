## Description: <br>
Rafter Security helps developers scan code and repositories for vulnerabilities, audit third-party skills, MCPs, and agent configs, evaluate shell commands, and generate secure design questions using the Rafter CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rafter](https://clawhub.ai/user/rafter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use Rafter Security to add CLI-backed security checks to agent workflows, including local secret scans, command-risk classification, third-party skill audits, and secure-design review prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the external Rafter CLI. <br>
Mitigation: Install and use the skill only when the Rafter CLI source is trusted. <br>
Risk: Remote scans may send code to Rafter's service when RAFTER_API_KEY is configured. <br>
Mitigation: Use local commands such as rafter secrets when remote analysis is not appropriate, and configure RAFTER_API_KEY only for repositories that may be sent to Rafter. <br>
Risk: Rafter agent initialization can enable hooks and integrations that affect command review behavior. <br>
Mitigation: Review what rafter agent init --all enables, or use opt-in --with-* flags for specific integrations. <br>
Risk: There is documentation ambiguity around whether one command path only classifies or may execute commands. <br>
Mitigation: Use rafter agent exec --dry-run when only command-risk classification is intended. <br>


## Reference(s): <br>
- [Rafter homepage](https://rafter.so) <br>
- [ClawHub skill page](https://clawhub.ai/rafter/rafter-security) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured audit-report sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Rafter CLI JSON output may be available for some commands; remote scanning requires RAFTER_API_KEY.] <br>

## Skill Version(s): <br>
0.8.9 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
