## Description: <br>
Track hours saved by AI-assisted work and calculate value using category-based hourly rates for ROI summaries and reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sergirostoll-coder](https://clawhub.ai/user/sergirostoll-coder) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Individuals, teams, and operators use this skill to log AI-assisted tasks, estimate hours saved, and produce value summaries that support business-case reporting. It is useful when an agent needs to maintain a local task-value ledger and export summaries as human-readable reports or dashboard-ready JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled data.json contains existing task history that may make reports reflect prior sample or publisher data rather than the user's own work. <br>
Mitigation: Review, clear, or replace data.json before first use when a clean ledger is required. <br>
Risk: Task descriptions and notes are persisted locally and may appear in Markdown reports or JSON exports. <br>
Mitigation: Avoid recording secrets, credentials, or highly sensitive business details in logged tasks or notes. <br>


## Reference(s): <br>
- [Value Tracker ClawHub release](https://clawhub.ai/sergirostoll-coder/value-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/sergirostoll-coder) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [CLI text summaries, Markdown reports, JSON exports, and local JSON configuration/data files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores task entries locally in data.json and reads category rates from config.json.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
