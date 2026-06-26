## Description: <br>
Fetch, analyze, chart, and track WHOOP health data including recovery, HRV, resting heart rate, sleep, strain, and workouts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brennaman](https://clawhub.ai/user/brennaman) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to WHOOP data, summarize recovery and sleep trends, generate charts, track health experiments, and optionally log daily metrics to Obsidian. The health interpretation is informational and should not be treated as medical advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional Obsidian logger may stage, commit, and push unrelated private notes when the configured vault is a Git repository. <br>
Mitigation: Use --dry-run first, inspect git status before enabling sync, and disable or remove automatic Git sync if the vault contains unrelated private content. <br>
Risk: WHOOP OAuth credentials are stored locally under ~/.config/whoop-skill/credentials.json. <br>
Mitigation: Protect the credentials file, grant only scopes the user is comfortable with, and re-authenticate or revoke access if credentials may be exposed. <br>
Risk: Health interpretations can be mistaken for medical advice. <br>
Mitigation: Present WHOOP analysis as informational trend guidance and direct users to qualified medical professionals for health concerns. <br>


## Reference(s): <br>
- [WHOOP Lab homepage](https://www.paulbrennaman.me/lab/whoop-skill) <br>
- [ClawHub WHOOP Lab release](https://clawhub.ai/brennaman/whoop-lab) <br>
- [WHOOP API Reference](artifact/references/api.md) <br>
- [WHOOP Health Analysis Guide](artifact/references/health_analysis.md) <br>
- [WHOOP Developer API documentation](https://developer.whoop.com/api) <br>
- [WHOOP Developer Dashboard](https://developer-dashboard.whoop.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, HTML files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON API responses, and generated HTML chart files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local WHOOP credentials, configuration, experiment records, HTML charts, and optional Obsidian daily notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
