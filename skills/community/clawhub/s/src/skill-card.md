## Description: <br>
Bridge macOS-only tools into a Linux OpenClaw gateway via SSH wrappers and connected Mac nodes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matthewxmurphy](https://clawhub.ai/user/matthewxmurphy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when a Linux OpenClaw gateway needs a repeatable way to call macOS-only command-line tools on trusted Mac nodes through SSH wrappers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent SSH wrappers can create durable remote access from the Linux gateway to a Mac node. <br>
Mitigation: Install wrappers only for trusted gateway and Mac accounts, use non-root accounts, and remove wrappers when they are no longer needed. <br>
Risk: Weak setup-value escaping can make untrusted hostnames or paths unsafe during wrapper generation. <br>
Mitigation: Do not pass hostnames, paths, or wrapper names from untrusted sources until the quoting behavior is fixed and reviewed. <br>
Risk: Broad tool wrappers such as brew or gh can expose more remote capability than a workflow needs. <br>
Mitigation: Prefer one narrow wrapper per tool, use dedicated SSH keys, and pin known hosts where practical. <br>


## Reference(s): <br>
- [Security Model](references/security-model.md) <br>
- [Publish Pattern](references/publish-pattern.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/matthewxmurphy/src) <br>
- [Publisher Profile](https://clawhub.ai/user/matthewxmurphy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and wrapper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces wrapper-oriented setup guidance for trusted Linux gateway to macOS node workflows.] <br>

## Skill Version(s): <br>
0.6.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
