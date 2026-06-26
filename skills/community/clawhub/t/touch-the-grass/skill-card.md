## Description: <br>
Touch The Grass helps users plan and complete low-dopamine, offline wellness activities, schedule them on Google Calendar, track points and streaks, and optionally verify completion through text, photos, or social posts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alannetwork](https://clawhub.ai/user/alannetwork) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and agents use this skill when a user reports stress, burnout, or a need to disconnect from work. It suggests time-appropriate analog or outdoor activities, can schedule them as calendar events, and tracks completion, mood check-ins, points, and streaks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calendar events could be created with the wrong date, time, or timezone. <br>
Mitigation: Confirm event details and timezone with the user before writing to Google Calendar. <br>
Risk: The skill may store personal routines, mood check-ins, and activity progress in agent memory. <br>
Mitigation: Keep stored progress minimal and use the skill only when the user wants ongoing wellness tracking. <br>
Risk: Photo or social-post verification can expose personal context. <br>
Mitigation: Offer text confirmation as the privacy-preserving path and avoid unnecessary description of personal details in images. <br>
Risk: Daily reminders may become unwanted or intrusive. <br>
Mitigation: Enable cron or heartbeat reminders only with user consent and stop prompting when the user declines for the day. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alannetwork/touch-the-grass) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Activity catalog](artifact/activities.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown conversation text with optional shell command blocks, configuration snippets, and calendar event details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request mood ratings, event timing, timezone confirmation, and text, photo, or social-post completion confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
