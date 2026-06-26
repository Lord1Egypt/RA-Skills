## Description: <br>
Operate Skool communities with onboarding, classroom planning, calendar cadence, official automations, and safer member lifecycle workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External community operators and agents use this skill to plan and run Skool groups, onboarding flows, classroom access, calendar cadence, and official automation workflows while keeping member-facing changes explicit and reviewable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live Skool operations such as invites, removals, access changes, AutoDM, Zapier, webhook, or billing-adjacent work can affect real members. <br>
Mitigation: Keep the skill advisory unless the user explicitly approves the exact member-facing action, preview the workflow, and confirm rollback steps before execution. <br>
Risk: Local Skool memory can become privacy-sensitive if it stores raw messages, credentials, payment details, or member dossiers. <br>
Mitigation: Store only group-level operating rules, approved defaults, automation boundaries, and incident lessons in ~/skool/ after user consent. <br>
Risk: Unsupported automation or stale platform assumptions can produce fragile workflows or incorrect access behavior. <br>
Mitigation: Use native Skool behavior and officially documented surfaces first, re-check current Skool docs for plan-gated or feature-specific behavior, and make unsupported limitations explicit. <br>


## Reference(s): <br>
- [ClawHub Skool release page](https://clawhub.ai/ivangdavila/skool) <br>
- [Skill homepage](https://clawic.com/skills/skool) <br>
- [Skool official help](https://help.skool.com) <br>
- [Official surface guidance](artifact/official-surface.md) <br>
- [Automation and integrations guidance](artifact/automation-and-integrations.md) <br>
- [Member lifecycle guidance](artifact/member-lifecycle.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with occasional inline shell commands and configuration paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use local notes under ~/skool/ after user consent; may reference official Skool help, Zapier, or approved webhook destinations when relevant.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
