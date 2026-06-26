## Description: <br>
Finds new upcoming IT events worldwide based on user-selected interests and location, avoids duplicates, and helps return official registration or payment links on request. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frankyjo](https://clawhub.ai/user/frankyjo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical community managers use this skill to find future IT conferences, meetups, workshops, webinars, and similar events for selected topics and locations. It supports one-time searches, recurring digests, deduplication through a local state file, and follow-up lookup of official registration or payment links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create a persistent weekly OpenClaw cron job. <br>
Mitigation: Enable recurring automation only after confirming the schedule, command, state file path, and deletion procedure; use one-time searches when persistent background execution is not wanted. <br>
Risk: Helper scripts create or update a local deduplication state file. <br>
Mitigation: Review memory/it-events-sent.json before and after runs when state retention or duplicate suppression needs to be audited. <br>
Risk: Artifact instructions and helper scripts differ on location handling; the scripts shown in evidence hardcode Ukraine while the skill text describes country or worldwide search. <br>
Mitigation: Confirm the intended location behavior before relying on script automation for non-Ukraine or worldwide event searches. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/frankyjo/searchitevents) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown digest with event details and links; helper scripts emit shell output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains deduplication state in memory/it-events-sent.json when searches or digests are run.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
