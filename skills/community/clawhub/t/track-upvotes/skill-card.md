## Description: <br>
Tracks Product Hunt launch upvotes, comments, rank, and simple trend data from public Product Hunt pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[3rdbrain](https://clawhub.ai/user/3rdbrain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Launch teams, founders, and growth operators use this Node.js CLI to check public Product Hunt post upvotes, comment counts, rank signals, and trend changes during launch monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release advertises Telegram alerts, but the reviewed files do not implement Telegram notifications. <br>
Mitigation: Use it as a manual Node.js CLI for checking public Product Hunt pages; do not rely on alert delivery unless a future version adds and documents that feature. <br>
Risk: Stats extraction depends on Product Hunt public page markup and may return missing fields if the page layout changes or the target URL is not a real Product Hunt post. <br>
Mitigation: Pass only real Product Hunt post URLs and review the returned fields before using them for launch decisions. <br>


## Reference(s): <br>
- [Product Hunt Launch Tracker on ClawHub](https://clawhub.ai/3rdbrain/track-upvotes) <br>
- [3rdbrain Publisher Profile](https://clawhub.ai/user/3rdbrain) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [CLI text and JavaScript objects containing status data, timestamps, and summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Trend history is held in memory for the current process; Telegram delivery is not implemented in the reviewed files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
