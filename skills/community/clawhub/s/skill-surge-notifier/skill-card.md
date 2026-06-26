## Description: <br>
Monitors ClawHub skill metrics and alerts when download growth exceeds 30%, downloads pass 50,000, stars pass 200, or new top 10 skills appear. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Gabriel-Kaufman](https://clawhub.ai/user/Gabriel-Kaufman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to monitor ClawHub trends, identify fast-growing skills, and surface relevance-ranked surge alerts for skills that may be worth reviewing or installing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts clawhub.ai to fetch public skill metrics. <br>
Mitigation: Run it only in environments where outbound access to clawhub.ai is acceptable. <br>
Risk: The skill creates local state, configuration, and profile files under ~/.skill-surge-notifier unless paths are overridden. <br>
Mitigation: Review SURGE_DIR, STATE_PATH, and CONFIG_PATH before scheduled use, and avoid putting secrets in profile descriptions or custom paths. <br>
Risk: The cron example appends command output to a local log file. <br>
Mitigation: Place scheduler logs in an approved location and rotate or clear them according to local retention policy. <br>


## Reference(s): <br>
- [Trending Skill Finder release page](https://clawhub.ai/Gabriel-Kaufman/skill-surge-notifier) <br>
- [ClawHub skills directory](https://clawhub.ai/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text CLI output with optional shell command examples and JSON-backed local configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public ClawHub skill metrics, writes local state and profile files, and can append scheduler logs when configured by the user.] <br>

## Skill Version(s): <br>
1.0.9 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
