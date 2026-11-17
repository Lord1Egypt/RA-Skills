## Description:

Automates daily WorkBuddy Buddy Station check-ins and cat-travel reward collection, with API access and a calibrated Windows desktop fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noaheleven](https://clawhub.ai/user/noaheleven)

### License/Terms of Use:

MIT-0

## Use Case:

WorkBuddy users on Windows use this skill to check in for daily points, review cat-travel status, and optionally claim travel rewards and send the cat on another trip. It can fall back to calibrated desktop clicks if API check-in fails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads or decrypts the local WorkBuddy login state and sends bearer credentials to official service endpoints.

Mitigation: Use only with an account you authorize, review credential access and endpoint use before installation, and avoid exposing local authentication files or output.

Risk: Optional external helper skills may access encrypted credentials or capture desktop screenshots.

Mitigation: Review the helper skills before enabling them; avoid them if their access is not acceptable.

Risk: Desktop automation can click the wrong control, store screenshots and state, or briefly create a Windows scheduled task during update recovery.

Mitigation: Calibrate and dry-run desktop clicks before execution; review stored screenshots and state, and check that the recovery task is removed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/noaheleven/skills/wb-buddy-checkin)
- [Windows desktop calibration guide](references/calibration.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Console status and optional JSON travel status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Check-in and travel actions can change account reward state; desktop fallback can save screenshots and calibration or recovery state locally.]

## Skill Version(s):

0.1.8 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
