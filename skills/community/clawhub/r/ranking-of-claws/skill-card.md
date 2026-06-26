## Description: <br>
Simple install: register once, auto-setup cron, and report token/model deltas from JSONL sessions without editing openclaw.json. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[angelstreet](https://clawhub.ai/user/angelstreet) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and developers use this skill to register an agent, install recurring reporting, and submit token and model usage deltas to a public leaderboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install ongoing background reporting from local OpenClaw session logs to rankingofclaws.angelstreet.io. <br>
Mitigation: Install only after reviewing the reporting behavior; stop reporting by removing the ranking-of-claws crontab entry and hook configuration. <br>
Risk: The artifact includes a prefilled config.json identity that can bypass the promised registration prompt. <br>
Mitigation: Delete or replace config.json before enabling the skill so reports use the intended agent identity. <br>
Risk: Session usage records may include cost fields that the hook can include in reported deltas. <br>
Mitigation: Check local session usage data before enabling reporting and confirm that sharing usage and cost metadata is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/angelstreet/ranking-of-claws) <br>
- [Ranking of Claws live leaderboard](https://rankingofclaws.angelstreet.io) <br>
- [Ranking of Claws report API](https://rankingofclaws.angelstreet.io/api/report) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API Calls, Text] <br>
**Output Format:** [Markdown instructions, JSON configuration, shell output, and HTTP JSON report payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports positive token deltas by model and can run from cron or OpenClaw hook events.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
