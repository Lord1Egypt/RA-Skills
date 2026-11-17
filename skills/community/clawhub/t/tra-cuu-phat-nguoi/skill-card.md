## Description:

Tra cuu phat nguoi phuong tien tai Viet Nam by license plate, with guidance to cross-check official sources when confirmation is needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ldt116](https://clawhub.ai/user/ldt116)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to check Vietnamese traffic-fine status by license plate, summarize returned violations, and advise users to confirm important results through official CSGT or registration sources.

### Deployment Geography for Use:

Vietnam

## Known Risks and Mitigations:

Risk: The lookup sends license plate details and any provided phone number to vnetraffic.org, which the artifact and security evidence identify as a third-party intermediary rather than an official government portal.

Mitigation: Tell users before lookup that data is sent to an intermediary, avoid collecting unnecessary phone numbers, and use official Vietnamese government or registration portals for final confirmation.

Risk: Intermediary lookup results may be incomplete, stale, unavailable, or blocked by endpoint errors and CAPTCHA on official portals.

Mitigation: Present results as intermediary data, recommend official cross-checking, and fall back to interpreting user-provided screenshots when automated lookup is unavailable.

## Reference(s):

- [CSGT official portal](https://www.csgt.vn)
- [VNeTraffic lookup endpoint](https://vnetraffic.org/wp-json/custom/v1/tra-cuu-csgt)
- [ClawHub skill page](https://clawhub.ai/ldt116/skills/tra-cuu-phat-nguoi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON lookup results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normalizes license plates, maps vehicle type arguments, and summarizes violation counts and records returned by the lookup endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
