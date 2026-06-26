## Description: <br>
Give your AI agent access to your health and fitness data from RUNSTR. Fetches workouts, habits, journal entries, mood, steps, and more from Nostr. Use when the user asks about their workouts, fitness history, health habits, mood tracking, or wants AI fitness coaching based on real data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheWildHustle](https://clawhub.ai/user/TheWildHustle) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users can let an agent fetch and analyze their RUNSTR fitness, habit, journal, mood, and step data from encrypted Nostr backups for coaching and personal health insight. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the user to provide a full Nostr private key for RUNSTR data access. <br>
Mitigation: Use a dedicated RUNSTR/Nostr identity rather than a main nsec, and install only if that level of access is acceptable. <br>
Risk: Sensitive RUNSTR health summaries may be saved for future conversations. <br>
Mitigation: Explicitly tell the agent not to store health summaries unless retention is intended. <br>
Risk: Pasted secrets and command arguments may appear in local or platform logs. <br>
Mitigation: Assume entered secrets can be logged and avoid using a primary identity or broadly trusted private key. <br>


## Reference(s): <br>
- [RUNSTR website](https://runstr.app) <br>
- [RUNSTR GitHub organization](https://github.com/RUNSTR) <br>
- [Nostr Army Knife install package](https://github.com/fiatjaf/nak) <br>
- [ClawHub skill page](https://clawhub.ai/TheWildHustle/runstr-fitness) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize sensitive health and fitness data from the user's RUNSTR backup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
