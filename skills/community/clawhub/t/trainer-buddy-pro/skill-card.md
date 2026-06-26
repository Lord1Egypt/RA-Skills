## Description: <br>
Trainer Buddy Pro helps an agent generate personalized workouts from gym equipment photos, track workout history and PRs, provide form cues, and adapt suggestions around user-reported injuries or limitations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External fitness users use this skill to create equipment-aware training sessions, log completed workouts, review progress, and receive general form and programming guidance. It is not a medical or certified personal-training substitute. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workout profiles can include sensitive body, injury, limitation, and training-history data. <br>
Mitigation: Keep core skill data local, use restrictive file permissions, and ask before saving injury or limitation details. <br>
Risk: Dashboard and cloud-sync materials can conflict with local-only privacy expectations by moving workout profile data into a database or hosted dashboard. <br>
Mitigation: Enable dashboard sync only with explicit user consent, minimize synced fields, and avoid uploading injury or limitation notes unless necessary. <br>
Risk: Fitness suggestions may be inappropriate for a user's medical condition, injury, or current ability. <br>
Mitigation: Present guidance as general fitness information, avoid diagnosis or rehabilitation protocols, and direct users to qualified healthcare professionals for pain, acute symptoms, or medical concerns. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nollio/trainer-buddy-pro) <br>
- [README](artifact/README.md) <br>
- [Security audit](artifact/SECURITY.md) <br>
- [Dashboard companion build spec](artifact/dashboard-kit/DASHBOARD-SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown responses with structured workout plans, progress summaries, JSON configuration examples, and occasional shell commands for setup or backup.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update local workout, profile, PR, and configuration files when the host agent allows file access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
