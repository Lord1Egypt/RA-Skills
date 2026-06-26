## Description: <br>
Call the Solvea Web App chat API to get AI customer-service replies for real customer-service questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Airoucat233](https://clawhub.ai/user/Airoucat233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Customer-service operators and OpenClaw agents use Solvea Chat to route messages from configured channels to the Solvea Web App chat API and return the platform's reply. It supports session reset handling and per-user conversation continuity for customer support workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan flagged review-worthy handling of API credentials used to call Solvea. <br>
Mitigation: Use a dedicated OpenClaw agent, avoid configuring secrets in shared or recorded terminals, and restrict permissions on the skill's .env file. <br>
Risk: Customer messages and API activity may be written to local logs while the skill handles support conversations. <br>
Mitigation: Review, disable, or redact solvea-chat.log before processing sensitive customer messages. <br>
Risk: Setup and uninstall flows can change local OpenClaw configuration and may delete a workspace directory when confirmed. <br>
Mitigation: Back up openclaw.json and workspace files before setup, and review uninstall prompts carefully before confirming deletion. <br>


## Reference(s): <br>
- [Solvea Chat API Spec](references/api-spec.md) <br>
- [Solvea](https://solvea.cx) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Plain text replies on stdout, stderr error messages, and Markdown setup guidance with shell and JSON examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains local session state for peer IDs and returns nonzero exit codes for network, authentication, or configuration failures.] <br>

## Skill Version(s): <br>
0.5.7 (source: server release metadata; artifact frontmatter reports 0.5.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
