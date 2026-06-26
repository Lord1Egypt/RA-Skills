## Description: <br>
Navigate Uber Eats in a live browser or app handoff to compare merchants, manage carts, and reach checkout safely. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to browse Uber Eats, compare merchants, prepare carts, verify checkout details, and recover from ordering issues in a live session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect real carts, delivery details, payments, and live orders when used with browser control. <br>
Mitigation: Keep the workflow browse-only unless the user asks for cart help, and require explicit confirmation before live order or delivery changes. <br>
Risk: Optional local memory could capture sensitive ordering information if used carelessly. <br>
Mitigation: Store only short preferences and troubleshooting notes; do not store secrets, payment data, verification codes, sensitive receipts, or full support transcripts. <br>
Risk: Blocked or unreliable web sessions can lead to incorrect assumptions about cart, address, or checkout state. <br>
Mitigation: Stop blind interaction, re-read the visible state, and switch to app handoff, manual guidance, or support recovery when the session is not trustworthy. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/uber-eats) <br>
- [Skill Homepage](https://clawic.com/skills/uber-eats) <br>
- [Uber Eats](https://www.ubereats.com) <br>
- [Uber Eats Help](https://help.uber.com/ubereats) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional local memory file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an approved browser or app session for live Uber Eats state; may use optional local notes in ~/uber-eats/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
