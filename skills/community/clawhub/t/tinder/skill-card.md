## Description: <br>
Coach Tinder goals with profile reviews, opener feedback, chat triage, and local experiments that improve matches and dates over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill as a Tinder coaching assistant to review profiles, draft profile-specific openers, triage chat momentum, plan low-friction dates, and maintain approved local experiment notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local coaching notes in ~/tinder/ can contain sensitive dating context if the user saves too much detail. <br>
Mitigation: Ask before creating or updating notes, save only durable summaries needed for coaching, avoid raw chats or intimate third-party details, and review or delete files when they are no longer needed. <br>
Risk: Profile, opener, chat, or date advice could misrepresent the user or create unsafe pressure if followed without review. <br>
Mitigation: Keep advice in the user's real voice, require explicit confirmation before send, unmatch, report, block, or local-write actions, and default first meetups to public, low-friction, easy-exit plans. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/tinder) <br>
- [Skill homepage](https://clawic.com/skills/tinder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown guidance with optional local note templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before creating or updating ~/tinder/ notes; no external requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
