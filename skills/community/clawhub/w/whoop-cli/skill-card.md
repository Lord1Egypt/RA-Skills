## Description: <br>
Helps agents operate the installed whoop CLI for WHOOP access, summaries, health flags, activity trends, exports, credential checks, and local skill installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andreasnlarsen](https://clawhub.ai/user/andreasnlarsen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to work with personal WHOOP data through the installed whoop CLI, including daily briefs, summaries, health flags, activity analysis, exports, and setup checks. It is intended for users who explicitly want agent assistance with WHOOP CLI workflows and accept the related health-data and credential-handling responsibilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help an agent operate workflows involving personal health data and authentication state. <br>
Mitigation: Install and use it only when agent assistance with WHOOP CLI workflows is intended, and review any export or skill-install command before running it. <br>
Risk: Improper credential handling could expose long-lived secrets or tokens. <br>
Mitigation: Use macOS Keychain or 1Password storage where possible, do not paste long-lived secrets into chat, and run first-time login locally. <br>
Risk: The local-vps secret-storage mode is a lower-security fallback. <br>
Mitigation: Use local-vps only with explicit acceptance of that tradeoff and prefer onepassword storage for Linux or OpenClaw deployments. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/andreasnlarsen/whoop-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON-producing CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may produce JSON from the whoop CLI; guidance emphasizes credential storage choices and personal health-data handling.] <br>

## Skill Version(s): <br>
0.5.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
