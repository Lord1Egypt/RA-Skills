## Description:

Guides an agent to plan tallow candle batches by calculating recipes, wick sizing, temperatures, timelines, logs, templates, and safety checklists while the human performs the physical candle-making steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to turn available animal fat and wick materials into planned candle batches for emergency, off-grid, or barter lighting. The agent supplies batch math, safety checklists, curing schedules, troubleshooting guidance, and inventory or trade templates while the user handles all hot-fat and open-flame work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer command is unpinned, so users could install an unexpected package version or source.

Mitigation: Install only from a trusted ClawHub/npm source, prefer a pinned or otherwise verified installer when available, and run without elevated privileges.

Risk: The workflow involves hot fat and open flame, which can cause burns, smoke exposure, or fire if handled incorrectly.

Mitigation: Follow the skill's safety notes, use appropriate ventilation and fire-suppression equipment, never leave melting fat unattended, and treat agent output as planning support rather than fire-safety judgment.

Risk: Filesystem-enabled workflows may create or update local batch logs, dashboards, inventory trackers, and templates.

Mitigation: Run the skill in an appropriate workspace and review created files before relying on or sharing them.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with checklists, batch calculations, logs, templates, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or maintain local batch logs, inventory trackers, progress dashboards, curing reminders, and barter templates through filesystem-enabled agent workflows.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
