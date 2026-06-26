## Description: <br>
Supply chain security hooks for Claude Code that intercept npm, pip, yarn, pnpm, and cargo install commands before execution and check packages for package age, typosquat similarity, install scripts, and optional Argus analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bkojusner](https://clawhub.ai/user/bkojusner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers using Claude Code use this skill to screen package-install commands before execution and warn or block packages with supply-chain risk signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The hook can block package installation commands based on supply-chain risk signals. <br>
Mitigation: Review the hook message and package details before retrying or bypassing a blocked install. <br>
Risk: When Argus is configured, package names, ecosystem, age, similarity target, and install-script status can be sent to the configured external endpoint. <br>
Mitigation: Leave Argus environment variables unset unless the endpoint is trusted to receive that package metadata. <br>


## Reference(s): <br>
- [Yeeth Claw on ClawHub](https://clawhub.ai/bkojusner/yeeth-claw) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text hook messages and Markdown installation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May warn or block package-install shell commands; optional Argus escalation requires user-configured environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
