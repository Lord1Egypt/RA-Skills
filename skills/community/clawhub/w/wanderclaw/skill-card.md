## Description: <br>
虾游 WanderClaw is a dormant OpenClaw knowledge-exploration agent that activates on explicit keywords, searches and fetches web sources, writes postcard-style knowledge digests, and can schedule recurring explorations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zzstart2](https://clawhub.ai/user/zzstart2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill to receive recurring, personalized knowledge discoveries as concise postcards, review prior discoveries, request deeper explorations, and manage favorites or blocked topics through chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install autonomous daily and weekly OpenClaw jobs that search the web, use model or search resources, and post results back to chat. <br>
Mitigation: Install only when recurring autonomous exploration is desired, then review the created cron jobs and remove or disable any schedules that do not match the user's intended cadence. <br>
Risk: The skill writes local interest and history data in a wanderclaw directory. <br>
Mitigation: Review the wanderclaw directory before relying on the skill, and delete or edit stored interest, history, or postcard files when the user wants to reset personalization. <br>
Risk: The skill can silently retry pending scheduled tasks and write a future prompt into shared agent memory. <br>
Mitigation: Inspect the pending-cron queue and any memory/YYYY-MM-DD.md nudge; remove those entries if the skill should act only when explicitly invoked. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zzstart2/wanderclaw) <br>
- [README](README.md) <br>
- [Explorer Workflow](references/EXPLORER.md) <br>
- [Soul Persona](references/SOUL.md) <br>
- [Postcard Format](references/postcard-format.md) <br>
- [Source List](references/sources.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and chat text with occasional shell command execution guidance and JSON-backed local state.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local wanderclaw state files and schedule OpenClaw cron jobs when activated.] <br>

## Skill Version(s): <br>
3.2.4 (source: server release metadata and CHANGELOG.md, released 2026-04-20) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
