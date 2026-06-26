## Description: <br>
Send a quick email via SkillBoss API Hub without a local mail client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quincygunter](https://clawhub.ai/user/quincygunter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent builders use this skill to send quick HTML email messages through the SkillBoss API Hub, including recipient, CC, BCC, subject, and body fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email contents, recipient addresses, CC, and BCC values are sent to the third-party SkillBoss API service. <br>
Mitigation: Use the skill only when SkillBoss/HeyBossAI is approved to process the intended email data, and avoid secrets, regulated data, or sensitive personal information unless that use is explicitly authorized. <br>
Risk: The skill requires SKILLBOSS_API_KEY, a sensitive credential. <br>
Mitigation: Store the API key in a secure environment variable or secret manager, prefer scoped or revocable credentials, and rotate or revoke the key if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/quincygunter/qui-email-send) <br>
- [SkillBoss API endpoint](https://api.heybossai.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces email-send usage guidance and API request examples; actual delivery depends on a valid SKILLBOSS_API_KEY and the third-party SkillBoss service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
