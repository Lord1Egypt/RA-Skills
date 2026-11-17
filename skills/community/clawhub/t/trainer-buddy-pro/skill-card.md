## Description:

Trainer Buddy Pro helps an agent create equipment-aware workout plans from gym photos, log training results, track personal records and progress, and adapt suggestions around reported injuries or limitations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT-0

## Use Case:

External fitness users use this skill in chat to receive personalized workout plans, log completed sessions, review progress, and get form cues based on local profile and workout history. It is an educational fitness assistant and is not a substitute for medical or professional training advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive fitness, body, and injury information in local profile and workout data.

Mitigation: Keep generated data local, restrict file permissions for runtime data, and use file-level or disk-level encryption for heightened privacy needs.

Risk: The optional dashboard kit can consume the full Trainer Buddy Pro data directory, including profile and injury data, if sync is enabled.

Mitigation: Use dashboard or cloud-backed sync only after reviewing the exact files being synced; prefer explicit allowlists or redaction for sensitive fields.

Risk: Documentation claims about local-only behavior may be broader than the optional dashboard behavior supports.

Mitigation: Review the dashboard manifest and companion spec before installation, and treat local-only guarantees as applying to the core skill unless the dashboard path is separately verified.

Risk: Workout and form guidance can be misapplied as medical, rehabilitation, or certified training advice.

Mitigation: Keep the medical disclaimer visible in agent behavior, avoid diagnosis or rehabilitation prescriptions, and refer users to qualified professionals for acute pain, numbness, dizziness, chest pain, or similar symptoms.

Risk: The setup documentation includes an uninstall command that removes the skill directory.

Mitigation: Back up user data and confirm the target path before running removal commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nollio/skills/trainer-buddy-pro)
- [Publisher Profile](https://clawhub.ai/user/nollio)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [Security Notes](artifact/SECURITY.md)
- [Dashboard Companion Spec](artifact/dashboard-kit/DASHBOARD-SPEC.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown workout plans and progress summaries, JSON data schemas, shell setup and backup commands, and dashboard configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and update local JSON data files for profiles, workout logs, and personal records when used by an agent.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
