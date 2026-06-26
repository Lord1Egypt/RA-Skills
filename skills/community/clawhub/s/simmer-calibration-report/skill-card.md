## Description: <br>
Run a calibration report on a Simmer trade journal, with win rate and expected value broken down by strategy, time of day, price band, and market type. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DjDyll](https://clawhub.ai/user/DjDyll) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and traders use this skill to analyze Simmer JSONL trade journals and identify where trading performance is strongest or weakest. It summarizes recent resolved trades across strategy, time, price band, day of week, and market type. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default sim mode can unexpectedly read live trading history if sim journal data is not found. <br>
Mitigation: Set CALIB_JOURNAL_PATH to the exact JSONL journal intended for analysis and confirm the selected file before running reports. <br>
Risk: The skill may process sensitive trading journal data. <br>
Mitigation: Review the skill before installation, run it only in a trusted workspace, and do not enable the daily cron until the journal path has been confirmed. <br>


## Reference(s): <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [ClawHub release page](https://clawhub.ai/DjDyll/simmer-calibration-report) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text report with setup and configuration commands; managed runs can also emit a compact JSON automaton summary.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires simmer-sdk and SIMMER_API_KEY. Reads a configured or auto-detected JSONL trade journal.] <br>

## Skill Version(s): <br>
1.0.4 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
