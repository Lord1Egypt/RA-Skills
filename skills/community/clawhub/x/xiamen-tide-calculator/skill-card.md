## Description:

Calculates Xiamen waters tide times and informational beachcombing guidance, including Gregorian-to-lunar date conversion, high and low tide times, beachcombing scores, location suggestions, equipment advice, and safety reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingwingshome](https://clawhub.ai/user/kingwingshome)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer Xiamen tide queries and plan beachcombing windows for specific dates. It provides informational tide timing, suitability scoring, multi-day comparisons, equipment suggestions, and safety reminders.

### Deployment Geography for Use:

Global users; guidance is localized to Xiamen, China waters.

## Known Risks and Mitigations:

Risk: Tide times and beachcombing recommendations can be safety-critical and may differ from real conditions.

Mitigation: Treat outputs as informational and verify official tide tables, weather, local warnings, and on-site conditions before going out.

Risk: The skill may execute local Python scripts and depends on the zhdate package.

Mitigation: Install and run it only after reviewing the disclosed scripts and dependency requirements for your environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kingwingshome/skills/xiamen-tide-calculator)
- [README_en.md](artifact/README_en.md)
- [SKILL_en.md](artifact/SKILL_en.md)
- [Usage guide](artifact/usage_guide.md)
- [New features guide](artifact/new_features_guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text with tide tables, ranked beachcombing recommendations, and safety reminders.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Python scripts and the zhdate dependency for lunar date conversion when script execution is available.]

## Skill Version(s):

3.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
