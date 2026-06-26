## Description: <br>
Verifies whether a Chinese mobile phone number, real name, and national ID number match telecom real-name authentication records, and can return carrier, province, and city information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xwzgit](https://clawhub.ai/user/xwzgit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to submit a consented Chinese phone number, real name, and ID card number to Juhe for telecom real-name verification. It is intended for lawful identity-check workflows that need a structured match result and optional carrier or location metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends full name, national ID number, and phone number to a third-party Juhe API. <br>
Mitigation: Use only with a lawful, consented purpose and avoid retaining shared terminal output or transcripts containing identity data. <br>
Risk: The security scan reports weak privacy controls for highly sensitive identity data. <br>
Mitigation: Mask or suppress sensitive inputs and outputs before using this skill in shared environments or saved logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xwzgit/telephone-verify) <br>
- [Juhe API reference](references/api.md) <br>
- [Juhe API endpoint](https://v.juhe.cn/telecom/query) <br>
- [Juhe website](https://www.juhe.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Code, Configuration, Text, JSON] <br>
**Output Format:** [Plain text or JSON verification result] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a JUHE_TELEPHONE_VERIFY_KEY API key; the metadata also references JUHE_TELEPHON_VERIFY_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
