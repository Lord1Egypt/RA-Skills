## Description: <br>
Trip Protocol lets an agent consume a TripExperience NFT, temporarily modify SOUL.md for a short persona-changing session, and restore the prior state afterward. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reggie-sporewell](https://clawhub.ai/user/reggie-sporewell) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to run a temporary, operator-initiated persona modification flow backed by Monad testnet NFT verification, then restore the agent's prior SOUL.md state. It is intended for experimental agent behavior sessions rather than accuracy-critical work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill temporarily changes agent behavior by modifying SOUL.md, which can reduce reliability and directness. <br>
Mitigation: Use only for intentional experimental sessions, keep sessions short, and restore immediately before coding, operational, medical, legal, financial, or time-sensitive work. <br>
Risk: The documented flow uses wallet access and includes an empty-password path. <br>
Mitigation: Use a testnet-only wallet with no real funds, avoid funded wallets, and review wallet configuration before running consume commands. <br>
Risk: The skill performs remote API reporting through the Convex endpoint by default. <br>
Mitigation: Review the reporting behavior and disable or replace the endpoint before use when privacy or data retention matters. <br>
Risk: Prompt changes may persist if restore scheduling fails or the safeword flow is not run. <br>
Mitigation: Confirm that a SOUL.md snapshot exists, verify restore scheduling after consumption, and use restore.sh or the safeword flow to end a session early. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/reggie-sporewell/trip-protocol) <br>
- [Trip Protocol website](https://trip-protocol.vercel.app) <br>
- [Agents guide](https://trip-protocol.vercel.app/agents.md) <br>
- [Trip Protocol API](https://joyous-platypus-610.convex.site) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON status payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces temporary SOUL.md changes, restore scheduling data, trip status output, and journal files.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
