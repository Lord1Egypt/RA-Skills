## Description:

问卷网（www.wenjuan.com）Skill helps agents create, publish, edit, inspect, report on, and export data from Wenjuan survey, assessment, vote, and form projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenjuanwang](https://clawhub.ai/user/wenjuanwang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to operate Wenjuan projects through guided workflows and Node.js scripts, including survey creation, publishing, project updates, reporting, raw data export, and response overview statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes install and update paths that can execute unreviewed remote instructions.

Mitigation: Install only from a trusted publisher and environment, prefer manual Node.js installation and npm ci, and review server-returned update commands before execution.

Risk: Changing WENJUAN_HOST or importing arbitrary remote JSON can increase exposure for sensitive networks or data.

Mitigation: Avoid setting WENJUAN_HOST unless required and prefer local JSON files over arbitrary import URLs.

Risk: The skill stores Wenjuan authentication material locally.

Mitigation: Protect and periodically remove ~/.wenjuan and the skill .wenjuan credentials when no longer needed.

## Reference(s):

- [问卷网 homepage](https://www.wenjuan.com)
- [ClawHub skill page](https://clawhub.ai/wenjuanwang/skills/wenjuan-survey)
- [Skill overview](references/skill_overview.md)
- [Authentication](references/auth.md)
- [Create survey workflow](references/create_survey.md)
- [Project JSON structure guide](references/project_json_structure_guide.md)
- [Export data](references/export_data.md)
- [Overview statistics](references/overview_stats.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON structures, local file paths, and Wenjuan project links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce survey links, report links, exported data files, QR-code poster image files, and instructions for managing local authentication state.]

## Skill Version(s):

1.0.15 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
