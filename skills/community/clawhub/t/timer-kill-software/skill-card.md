## Description: <br>
关机吧人类 is a paid timer assistant that helps users schedule closing selected categories of desktop software after payment verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[w16638771062](https://clawhub.ai/user/w16638771062) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to create a paid order, complete payment, and run a timer that closes game, office, chat, entertainment, or all configured software categories. It is intended for users who want an enforced stop time for late-night computer use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment and order data is sent to a hardcoded server over unencrypted HTTP. <br>
Mitigation: Use only if the user trusts the publisher and accepts the security guidance in the ClawScan summary; avoid sharing sensitive payment data beyond what the payment flow requires. <br>
Risk: The skill forcibly closes selected applications, which can cause loss of unsaved work. <br>
Mitigation: Ask the user to save work and confirm the software category and timing before running the service command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/w16638771062/timer-kill-software) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and payment workflow details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces order identifiers, payment status text, and process-closing command guidance for the agent to relay to the user.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
