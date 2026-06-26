## Description: <br>
Operate the saizeriya.js command-line interface on behalf of a user for Saizeriya mobile-ordering sessions, including session start or resume, state inspection, cart management, receipt details, and CLI command calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nakasyou](https://clawhub.ai/user/nakasyou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to run a Saizeriya ordering CLI carefully on the user's behalf, including reading session state, looking up item codes, managing a cart, and submitting confirmation-gated restaurant actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a live restaurant ordering session, including actions that submit orders or call staff. <br>
Mitigation: Require explicit user confirmation before submit, call staff, or call dessert commands, and state the exact real-world action before running it. <br>
Risk: QR/session data and local session storage may expose or affect the wrong table if reused incorrectly. <br>
Mitigation: Use only QR or session data supplied for the intended table, treat scanned QR values as untrusted until passed to the requested Saizeriya command, and consider a dedicated SAIZERIYA_CLI_HOME when session storage isolation matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nakasyou/saizeriya) <br>
- [qr-scanner-cli](https://github.com/victorperin/qr-scanner-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke npx or bunx commands and continue interactive CLI sessions through stdin when needed.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
