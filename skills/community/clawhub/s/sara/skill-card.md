## Description: <br>
Quiet logic guard for risky multi-skill workflows. Checks order before delete, send, booking, publishing, or other high-impact actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zc502](https://clawhub.ai/user/zc502) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Sara to audit risky multi-step tool plans before actions such as deletion, publishing, booking, payment, or sensitive data access. It returns warnings and a safer suggested order when a proposed sequence violates its ordering rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sara can suggest safer ordering, but it cannot guarantee that a proposed action is appropriate, authorized, or reversible. <br>
Mitigation: Review plans involving deletion, publishing, payments, scheduling, or private data before allowing the agent to continue. <br>
Risk: A safe ordering result may still include a high-impact or irreversible action. <br>
Mitigation: Ask for confirmation before continuing when the workflow touches destructive, externally visible, permissioned, or sensitive operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zc502/sara) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON, text] <br>
**Output Format:** [JSON audit results and concise Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local deterministic audit over an ordered list of proposed tools or steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact frontmatter and changelog describe 0.1.0 preview behavior) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
