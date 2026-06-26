## Description: <br>
vn.py open-source quantitative trading framework guidance for CTA, spread, options, broker gateway, data management, and strategy examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coderwpf](https://clawhub.ai/user/coderwpf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative trading practitioners use this skill to get vn.py setup guidance, strategy templates, broker gateway configuration examples, and operational reminders for testing or running trading workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broker connection and strategy-start examples could lead to real financial actions if used with live accounts. <br>
Mitigation: Review before installation or use, start with paper trading or SimNow-style test accounts, require explicit confirmation before connecting or starting strategies, and keep a fast stop path available. <br>
Risk: Broker credentials may be exposed if copied directly into examples or shared with an agent session. <br>
Mitigation: Store credentials in a secret manager or environment variables and avoid placing secrets directly in prompts, code snippets, or committed files. <br>
Risk: Unpinned trading dependencies can change behavior across installs. <br>
Mitigation: Pin dependency versions and validate the environment before using the skill for brokerage-connected workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/coderwpf/vnpy) <br>
- [vn.py homepage](https://www.vnpy.com) <br>
- [vn.py documentation](https://www.vnpy.com/docs/cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides examples and recommendations; users must review before connecting brokerage accounts or starting strategies.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
